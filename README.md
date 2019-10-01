# CO2Meter

Python Module to use co2meters like the 'AirCO2ntrol Mini' from TFA Dostmann with USB ID `04d9:a052`. There are also other modules using the same interface.

This module supports Python 2.7 and 3.x.

## Attribution

- Reverse Engineering of the protocol and initial code done by [Henryk Plötz](https://github.com/henryk). 
- Read all about it at [hackaday](https://hackaday.io/project/5301-reverse-engineering-a-low-cost-usb-co-monitor)
- Code derived from [this article](https://hackaday.io/project/5301-reverse-engineering-a-low-cost-usb-co-monitor/log/17909-all-your-base-are-belong-to-us)
- This repository is a fork of [Michael Nosthoff](https://github.com/heinemml/CO2Meter)'s repo

## Mini CO2 Monitor specification

This is taken from [product page](https://www.tfa-dostmann.de/en/produkt/co2-monitor-airco2ntrol-mini/) and linked Instruction manual.

Traffic LEDs thresholds:

- Green -- CO2 concentration below 800 ppm
- Yellow -- CO2 concentration between 800 ppm and 1200 ppm
- Red -- CO2 concentration above 1200 ppm

Specified operation / measurement ranges:

- Temperature 0°C...50°C
- CO2 concentration -- 0 ... 3000 ppm
  - Resolution of 1 ppm at 0 ... 1000 ppm
  - Resolution of 10 ppm at 1001 ... 3000 ppm

## Install

You can install this lib in standard way, but it is typically enough to just clone the repo and run from it. To allow non root users, you will probably need to install `udev` rules from `docs/99-co2monitor.rules` to `/etc/udev/rules.d/99-co2monitor.rules`. Depending on your system, you may need to run

```bash
udevadm control --reload-rules && udevadm trigger
```

## Usage

```python
from CO2Meter import *
import time
sensor = CO2Meter("/dev/hidraw0")
while True:
    time.sleep(2)
    sensor.get_data()
```

The device writes out one value at a time. So we need to parse some data until we have co2 and temperature. Thus the get_data() method will initially return none or only on value (whichever comes first). When you just need one measurement you should wait some seconds or iterate until you get a full reading. If you just need co2 a call to `get_co2` might speed things up.

### Callback

You can pass a callback to the constructor. It will be called when any of the values is updated. The parameters passed are `sensor` and `value`. `sensor` contains one of these constants:

```python
CO2METER_CO2 = 0x50
CO2METER_TEMP = 0x42
CO2METER_HUM = 0x44
```

### Error handling

In Case the device can't be read anymore (e.g. it was unplugged) the worker thread will end in the background. Afterwards calls to any of the `get_*` functions will throw an `IOError`. You will need to handle any reset, making sure that the device is there etc yourself.
