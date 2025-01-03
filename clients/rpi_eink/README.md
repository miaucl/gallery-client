# rpi-eink

This build is based on a Raspberry Pi and an eink display. It also features low-power using a watchdog to periodically power the device.

## Hardware

Raspberry PIs

- Raspberry Pi Zero v2
- others fine as well I guess

Displays

- [4inch_e-Paper_HAT+](https://www.waveshare.com/wiki/4inch_e-Paper_HAT%2B_(E)_Manual#Python)
- [7.3inch_e-Paper_HAT](https://www.waveshare.com/wiki/7.3inch_e-Paper_HAT_(E)_Manual#Python)

Watchdog Timer

- [Adafruit TPL5110 Low Power Timer Breakout](https://www.adafruit.com/product/3435) using an external resistor of [180kOhm](https://learn.adafruit.com/adafruit-tpl5110-power-timer-breakout/usage)
- [74HC74 D-FlipFlop](https://www.ti.com/lit/ds/symlink/sn74hc74-ep.pdf?ts=1735254685546&ref_url=https%253A%252F%252Fwww.google.com%252F) with some further components such as a `100kOhm` and a `10kOhm` resistor, and a `100nF` capacitor.

Power

[USB-C Breakout Board](https://www.adafruit.com/product/4090)

## RC Time

Use following page to calculate your POR circuit (recommended >10ms): <https://www.digikey.com/en/resources/conversion-calculators/conversion-calculator-time-constant>

## Configuration

Use the package either directly as package from your script or with env variables and the main entry.

Example .env file:

```txt
MODEL=rpi_eink_4in0e|rpi_eink_7in3e
PIC_PATH=/path/to/pic.bmp
PIC_URL=http://pic.url/img.bmp
PIC_URL_HEADER=AUTHORIZATION: BEARER QWER
DONE_PIN=12
```

## Misc

Use `last reboot` to see last boots and verify correct timer behaviour.

There are demo scripts `scripts/epd_{4in0e|7in3e}_test.py` to show the possibilities and verify the setup.

There is another script `scripts/simple_pic_{4in0e|7in3e}.py` to show a simple bmp image and the the verify that the image is usable.
