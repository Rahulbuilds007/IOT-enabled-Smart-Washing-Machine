import serial
import json
import paho.mqtt.client as mqtt

ACCESS_TOKEN = "ffr9jeaa97crdrvyh6s8"

SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 9600

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.connect("localhost",1883,60)

print("Connected to ThingsBoard")

while True:

    line = ser.readline().decode().strip()

    if line:

        try:
            vibration,temp1,temp2,load = line.split(",")

            data = {
                "vibration": float(vibration),
                "temperature1": float(temp1),
                "temperature2": float(temp2),
                "load": float(load)
            }

            client.publish("v1/devices/me/telemetry", json.dumps(data))

            print("Sent:",data)

        except:
            print("Invalid data:",line)
