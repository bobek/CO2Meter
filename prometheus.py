#!/bin/env python
from CO2Meter import *
from prometheus_client import start_http_server, Gauge
import time


def process_loop():
    Meter = CO2Meter("/dev/hidraw3")

    temperature = Gauge('temperature', 'Measured tempeterature')
    co2 = Gauge('co2', 'Measured CO2 level')
    humidity = Gauge('humidity', 'Measured humidity level')

    while True:
        measurement = Meter.get_data()
        print(measurement)
        if 'co2' in measurement:
            co2.set(measurement['co2'])
        if 'temperature' in measurement:
            temperature.set(measurement['temperature'])
        if 'humidity' in measurement:
            humidity.set(measurement['humidity'])
        time.sleep(5)


if __name__ == '__main__':
    start_http_server(7878)
    process_loop()
