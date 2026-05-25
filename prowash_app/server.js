
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

app.use(express.static(path.join(__dirname, 'public')));

// --- MACHINE STATE ---
let machine = {
    power: false,
    setupComplete: false,
    isRunning: false,
    isPaused: false,
    timeLeft: 45 * 60,
    totalDuration: 45 * 60,
    status: "READY",
    mode: 'MANUAL',
    
    // UPDATED DEFAULTS: Temp is now index 1 (40°C) because scale is 0-2
    settings: { temp: 1, rinse: 1, spin: 2, soil: 1 },
    
    options: {
        preSoak: false, delayEnd: false, steam: false, 
        drumLight: false, superSpeed: false, smartControl: false
    }
};

let timerInterval = null;

io.on('connection', (socket) => {
    socket.emit('update', machine);

    socket.on('setSetting', (data) => {
        if (machine.isRunning || !machine.power) return;
        machine.settings[data.type] = parseInt(data.value);
        recalculateTime();
        io.emit('update', machine);
    });

    socket.on('selectStartMode', (selectedMode) => {
        if (!machine.power) return;
        machine.mode = selectedMode;
        machine.setupComplete = true;
        if(selectedMode === 'AUTO') {
            // UPDATED AUTO DEFAULTS: Temp 1 = 40°C
            machine.settings = { temp: 1, rinse: 2, spin: 3, soil: 2 };
            recalculateTime();
        }
        io.emit('update', machine);
    });

    socket.on('toggleOption', (opt) => {
        if (!machine.power || machine.isRunning) return; 
        machine.options[opt] = !machine.options[opt];
        recalculateTime();
        io.emit('update', machine);
    });

    socket.on('togglePlay', () => {
        if (!machine.power) return;
        if (!machine.isRunning) startCycle();
        else {
            machine.isPaused = !machine.isPaused;
            machine.status = machine.isPaused ? "PAUSED" : "RUNNING";
            io.emit('update', machine);
        }
    });

    socket.on('togglePower', () => {
        machine.power = !machine.power;
        if (!machine.power) {
            resetMachine();
            machine.setupComplete = false;
        }
        io.emit('update', machine);
    });

    socket.on('setMode', (m) => {
        if (!machine.power || machine.isRunning) return;
        machine.mode = m;
        if(m === 'AUTO') { 
            machine.settings = { temp: 1, rinse: 2, spin: 3, soil: 2 }; 
            recalculateTime();
        }
        io.emit('update', machine);
    });
});

function recalculateTime() {
    let base = 25; 
    base += machine.settings.temp * 5;
    base += machine.settings.rinse * 12;
    base += machine.settings.spin * 3;
    base += machine.settings.soil * 8;
    
    if (machine.options.steam) base += 20;
    if (machine.options.preSoak) base += 15;
    if (machine.options.superSpeed) base -= 10;
    if (base < 15) base = 15;
    
    machine.timeLeft = base * 60;
    machine.totalDuration = machine.timeLeft;
}

function startCycle() {
    machine.isRunning = true;
    machine.isPaused = false;
    machine.status = "WASHING";
    clearInterval(timerInterval);
    timerInterval = setInterval(() => {
        if (machine.isRunning && !machine.isPaused && machine.power) {
            if (machine.timeLeft > 0) {
                machine.timeLeft--;
                io.emit('update', machine);
            } else {
                machine.status = "END";
                machine.isRunning = false;
                clearInterval(timerInterval);
                io.emit('update', machine);
            }
        }
    }, 1000);
}

function resetMachine() {
    machine.isRunning = false;
    machine.isPaused = false;
    machine.status = "OFF";
    clearInterval(timerInterval);
}

server.listen(3000, () => console.log('ProWash Slider Edition running on 3000'));

