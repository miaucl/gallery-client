"""Simple pic test."""

#!/usr/bin/python
import logging
import os
import sys
import time

from PIL import Image

basedir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "rpi_eink"
)
if os.path.exists(basedir):
    sys.path.append(basedir)
print(basedir)

from waveshare_epd import epd4in0e  # type: ignore # noqa: E402

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    pic = sys.argv[1]
    if not pic or not os.path.exists(pic):
        raise ReferenceError(f"Pic {pic} not found")
    print(f"Show pic: {pic}")

    try:
        logging.info("epd4in0e Simple pic")

        epd = epd4in0e.EPD()
        logging.info("init and Clear")
        epd.init()
        epd.Clear()

        # read bmp file
        logging.info("2.read bmp file")
        Himage = Image.open(pic)
        epd.display(epd.getbuffer(Himage))
        time.sleep(3)

        logging.info("Goto Sleep...")
        epd.sleep()

    except OSError as e:
        logging.info(e)
