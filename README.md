# 🧺 AI-Enabled Smart Washing Machine

### Real-Time Predictive Maintenance using Digital Twin & Edge Computing

---

## 🚀 Overview

This project presents an **AI-enhanced smart washing machine system** that replaces the original proprietary controller with an **open hardware + software architecture** using:

* Arduino Uno (low-level control)
* Raspberry Pi 4 (processing + UI + ML)
* Machine Learning (cloth dirt classification)
* IoT Digital Twin (ThingsBoard)

The system enables **real-time monitoring, intelligent decision-making, and predictive maintenance** for a conventional washing machine.

> This project demonstrates how legacy appliances can be transformed into smart systems using embedded systems and AI.

---

## 🧠 Key Features

* 🤖 **AI Mode** – Automatically selects wash settings based on cloth dirt level
* ⚙️ **Manual Mode** – User-configurable washing parameters
* 📡 **Real-time Sensor Monitoring**
* 🧺 **Load Detection (Weight-based)**
* 🌡️ Temperature, Current & Vibration Monitoring
* ⚡ Fault Detection & Safety Mechanisms
* ☁️ **Digital Twin using ThingsBoard**
* 🖥️ Touchscreen UI running on Raspberry Pi

---

## 🏗️ System Architecture

```
Sensors + Actuators (Washing Machine)
        ↓
Arduino Uno (Control Layer)
        ↓
USB Serial Communication
        ↓
Raspberry Pi 4
   ├── Node.js UI (Touchscreen)
   ├── ML Model (TFLite)
   └── Python + OpenCV
        ↓
ThingsBoard (Digital Twin Dashboard)
```

The system operates in **three layers**:

* Hardware Control Layer (Arduino)
* Processing + UI Layer (Raspberry Pi)
* AI Inference Layer (ML Model)

---

## 🔧 Hardware Components

* Arduino Uno R3
* Raspberry Pi 4 (4GB)
* 30A Relays (Motor Control)
* 5A Relays (Valve + Brake)
* Load Cell + HX711
* DS18B20 Temperature Sensor
* ACS712 Current Sensor
* Piezoelectric Vibration Sensor
* Water Level Sensor
* Camera Module

---

## 💻 Software Stack

* **Node.js + Express** → UI & control server
* **Python + OpenCV** → Image processing
* **TensorFlow Lite** → ML inference
* **Serial Communication (USB)** → Arduino ↔ Pi
* **ThingsBoard** → Digital twin dashboard

---

## 🤖 Machine Learning

* Model: **MobileNetV2 (Transfer Learning)**
* Classes:

  * Lightly Dirty
  * Dirty
  * Moderately Dirty
  * Heavily Dirty
* Accuracy: **~84.7%**
* Inference Speed: **~8 FPS on Raspberry Pi**

The model analyzes camera input and automatically configures:

* Water Temperature
* Water Level
* Spin Speed
* Rinse Cycles

---

## ⚙️ Working Modes

### 🟢 Manual Mode

User selects:

* Temperature
* Water level
* Spin speed
* Rinse cycles

### 🔵 AI Mode

* Camera captures cloth image
* ML model predicts dirt level
* System auto-configures wash parameters

---

## ☁️ Digital Twin (ThingsBoard)

* Real-time telemetry monitoring
* Sensor data visualization
* System debugging without hardware interaction
* Mirrors real machine behavior

This enables **predictive maintenance and performance tracking**.

---

## 📊 Results

* ✔️ Bidirectional motor control (CW/CCW)
* ✔️ Sensor accuracy:

  * Load Cell: ±1.5%
  * Temperature: ±0.5°C
* ✔️ ML Accuracy: ~84.7%
* ✔️ UI Response: <100ms
* ✔️ Real-time communication latency: <20ms

The system successfully executed complete wash cycles in both manual and AI modes.

---

## 📁 Project Structure

```
iot-washing-machine/
│
├── FINAL_CODE_WITH_CURRENT_SENSOR/
├── ML_MODEL/
├── prowash_app/
├── thingsboard_project/
├── washing machine_photos/
├── README.md
└── .gitignore
```

---

## 🛠️ Setup Instructions

### 1. Clone Repository

```
git clone https://github.com/YOUR_USERNAME/iot-washing-machine.git
cd iot-washing-machine
```

### 2. Run Web App

```
cd prowash_app
npm install
node server.js
```

### 3. Run IoT Script

```
cd thingsboard_project
python send_data.py
```

### 4. Run ML Model

```
cd ML_MODEL
python inference_server.py
```

---

## 👨‍💻 My Contribution (Rahul Chawla)

I worked extensively on **hardware integration, system control, and Raspberry Pi-based deployment**, including:

### 🔧 Hardware & Embedded Systems

* Designed and implemented **relay-based control system**
* Controlled:

  * Wash motor (CW/CCW)
  * Inlet valve
  * Drain system
  * Brake mechanism
* Ensured **safe interfacing with high-voltage components**

### 📡 Sensor Integration

* Integrated and calibrated:

  * Water level sensor
  * Current sensor
  * Temperature sensor
  * Vibration sensor
* Achieved accurate real-time data acquisition

### 🧠 System Integration

* Established **Arduino ↔ Raspberry Pi communication**
* Handled **serial protocol and synchronization**
* Performed system debugging and testing

### 🖥️ Raspberry Pi (Your extra contribution 🔥)

* Setup Raspberry Pi OS and environment
* Helped run:

  * **UI (Node.js interface)**
  * **Machine Learning inference**
* Assisted in real-time execution and integration of ML with system

### 📊 Demonstration & Testing

* Demonstrated hardware working and wash cycles
* Assisted in live system debugging
* Helped showcase sensor data and real-time monitoring

> This contribution reflects hands-on work in embedded systems, IoT integration, and edge AI deployment.

---

## 🔮 Future Scope

* 📱 Mobile App Integration
* ☁️ Cloud-based monitoring (MQTT)
* ⚡ Energy optimization
* 🎤 Voice control
* 🧵 Fabric type detection

---

## 👥 Team

* Rahul Chawla
* Kaushal Mishra
* Rishabh Singh
* Rudranil Maji

---

## 📜 License

This project is developed for academic and research purposes.

---

## ⭐ Final Note

This project showcases a **complete integration of IoT, Embedded Systems, Machine Learning, and Web Technologies** to build a real-world smart appliance system.
