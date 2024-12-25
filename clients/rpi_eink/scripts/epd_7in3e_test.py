"""Official test script."""

#!/usr/bin/python
import logging
import os
import sys
import time

from PIL import Image, ImageDraw, ImageFont

picdir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "pic"
)
basedir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "rpi_eink"
)
if os.path.exists(basedir):
    sys.path.append(basedir)

from waveshare_epd import epd7in3e  # type: ignore # noqa: E402

logging.basicConfig(level=logging.DEBUG)


try:
    logging.info("epd7in3e Demo")

    epd = epd7in3e.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    font24 = ImageFont.truetype(os.path.join(picdir, "Font.ttc"), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, "Font.ttc"), 18)
    font40 = ImageFont.truetype(os.path.join(picdir, "Font.ttc"), 40)

    # Drawing on the image
    logging.info("1.Drawing on the image...")
    Himage = Image.new(
        "RGB", (epd.width, epd.height), epd.WHITE
    )  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    draw.text((5, 0), "hello world", font=font18, fill=epd.RED)
    draw.text((5, 20), "7.3inch e-Paper (e)", font=font24, fill=epd.YELLOW)
    draw.text((5, 45), "微雪电子", font=font40, fill=epd.GREEN)
    draw.text((5, 85), "微雪电子", font=font40, fill=epd.BLUE)
    draw.text((5, 125), "微雪电子", font=font40, fill=epd.BLACK)

    draw.line((5, 170, 80, 245), fill=epd.BLUE)
    draw.line((80, 170, 5, 245), fill=epd.YELLOW)
    draw.rectangle((5, 170, 80, 245), outline=epd.BLACK)
    draw.rectangle((90, 170, 165, 245), fill=epd.GREEN)
    draw.arc((5, 250, 80, 325), 0, 360, fill=epd.RED)
    draw.chord((90, 250, 165, 325), 0, 360, fill=epd.YELLOW)
    epd.display(epd.getbuffer(Himage))
    time.sleep(3)

    # read bmp file
    logging.info("2.read bmp file")
    Himage = Image.open(os.path.join(picdir, "7in3e", "01.bmp"))
    epd.display(epd.getbuffer(Himage))
    time.sleep(3)

    logging.info("Clear...")
    epd.Clear()

    logging.info("Goto Sleep...")
    epd.sleep()

except OSError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd7in3e.epdconfig.module_exit(cleanup=True)  # type: ignore
    sys.exit()