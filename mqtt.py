#!/bin/env python
from CO2Meter import *
import paho.mqtt.client as mqttClient
import time

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected
        Connected = True
    else:
        print("Connection failed")

Connected = False   #global variable for the state of the connection
Meter = CO2Meter("/dev/hidraw3")

client = mqttClient.Client()
client.on_connect= on_connect
client.connect("10.0.0.250", port=1883)

client.loop_start()

while Connected != True:
    time.sleep(0.1)

try:
    while True:
        measurement = Meter.get_data()
        print(measurement)
        if 'co2' in measurement:
          client.publish("home/livingroom/co2", measurement['co2'])
        if 'temperature' in measurement:
          client.publish("home/livingroom/temperature", measurement['temperature'])
        if 'humidity' in measurement:
          client.publish("home/livingroom/humidity", measurement['humidity'])
        time.sleep(5)
except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()


