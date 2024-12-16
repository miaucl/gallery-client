# rpi-eink

This build is based on a Raspberry Pi and an eink display. It also features low-power using a watchdog to periodically power the device.

## Hardware

Raspberry PIs

- Raspberry Pi Zero v2
- others fine as well I guess

Displays

- [4inch_e-Paper_HAT+](https://www.waveshare.com/wiki/4inch_e-Paper_HAT%2B_(E)_Manual#Python)
- [7.3inch_e-Paper_HAT](https://www.waveshare.com/wiki/7.3inch_e-Paper_HAT_(E)_Manual#Python) (coming soon)

Watchdog Timer

- [Adafruit TPL5110 Low Power Timer Breakout](https://www.adafruit.com/product/3435) using an external resistor of [180kOhm](https://learn.adafruit.com/adafruit-tpl5110-power-timer-breakout/usage)
- (Optional) Delay circuit if your pins are floating at the beginning or even switch to high for a certain amount of time (see example). If not needed, remove C1 and R2 and set R3=0Ohm.

Power

[(Optionally) USB-C Breakout Board](https://www.adafruit.com/product/4090)

## Wiring

![Circuit](./circuit.png)

## Limitations

### Possible delay values

Currently, the slowest the timer can go is every 2h, therefore an additional logic is implemented to quickly check and shutdown based on a high level updated frequency defined on python level.

You have to use one of the GPIOs from [9..27] for the Done pin, as they are the only one per default pulled to GND.

### GPIOs state unknown (example RPi)

We need to use a high enough capacity C1 to bridge the RPi GPIO switching to HIGH for about 1s, but still have a low enough R3 to be able to trigger the Done pin.

Using the delay circuit, we assume that: The capacitor is considered "fully charged" after about 5 time constants (5τ), where τ=RC.

We observe, that with values C1=470uF and R1=10kOhm, we survive the startup and take about 4s to trigger the Done pin.

## Configuration

Use the package either directly as package from your script or with env variables and the main entry.

Example .env file:

```txt
PIC_PATH=/path/to/pic.bmp
PIC_URL=http://pic.url/img.bmp
PIC_URL_HEADER=AUTHORIZATION: BEARER QWER
DONE_PIN=12
```

## Misc

Use `last reboot` to see last boots and verify correct timer behaviour.

There is a demo script `scripts/epd_4in0e_test.py` to show the possibilities and verify the setup.

There is another script `scripts/simple_pic.test.py` to show a simple bmp image and the the verify that the image is usable.
