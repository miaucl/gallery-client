"""Init module."""

#!/usr/bin/python
from dataclasses import dataclass
import hashlib
from io import BytesIO
import logging
import os
from pathlib import Path
import time

from gpiozero import OutputDevice
from PIL import Image
import requests

from .waveshare_epd import epd4in0e, epd7in3e

_LOGGER = logging.getLogger(__name__)


@dataclass
class epd4in0e_consts:
    """Constants for the 4.0 inch e-Paper."""

    model: str = "rpi_eink_4in0e"
    height: int = 400
    width: int = 600
    rotation: int = -90


@dataclass
class epd7in3e_consts:
    """Constants for the 7.3 inch e-Paper."""

    model: str = "rpi_eink_7in3e"
    height: int = 480
    width: int = 800
    rotation: int = -90


FLAG_FILE = "/var/gallery-client/gallery-client-rpi-eink"


def refresh_client(
    model: str,
    path: str | None = None,
    url: str | None = None,
    url_headers: list[str] = [],
    done_pin: int | None = None,
) -> None:
    """Refresh the client."""
    if not path and not url:
        raise ReferenceError(
            "At least one of 'path' or 'url' must be set to refresh the client."
        )

    if model == epd4in0e_consts.model:
        epd = epd4in0e
        consts = epd4in0e_consts
    elif model == epd7in3e_consts.model:
        epd = epd7in3e
        consts = epd7in3e_consts
    else:
        raise ValueError(f"Invalid model: {model}")
    _LOGGER.info("Load model: %s", model)

    image: Image.Image | None = None
    try:
        if path:
            _LOGGER.info("Loading image from path: %s", path)
            image = load_image_from_path(path)
        elif url:
            _LOGGER.info("Loading image from url: %s", url)
            image = load_image_from_url(url, url_headers)

    except ReferenceError:
        _LOGGER.info(
            "Due to ReferenceError caught, we just shutdown and try again later."
        )
        if done_pin:
            enable_done_pin(done_pin)
        return

    if not image:
        _LOGGER.exception("'image' is None, which should not happen, aborting...")
        if done_pin:
            enable_done_pin(done_pin)
        return

    if image.format != "BMP":
        raise ValueError(
            f"The image is not a BMP file. Detected format: {image.format}"
        )

    w, h = image.size
    if h > w:
        image = image.rotate(consts.rotation, expand=True)
    if h != consts.height:
        raise ValueError(f"The image height '{h}' must be '{consts.height}'")
    if w != consts.width:
        raise ValueError(f"The image width '{w}' must be '{consts.width}'")

    image_hash = hashlib.sha256(image.tobytes()).hexdigest()
    Path(os.path.dirname(FLAG_FILE)).mkdir(parents=True, exist_ok=True)
    if os.path.exists(FLAG_FILE):
        with open(FLAG_FILE) as f:
            saved_hash = f.read().strip()

        if image_hash == saved_hash:
            _LOGGER.info("Image hash matches the saved hash, no refresh needed.")
            if done_pin:
                enable_done_pin(done_pin)
            return

    with open(FLAG_FILE, "w") as f:
        f.write(image_hash)
    _LOGGER.info("New hash written to %s: %s", FLAG_FILE, image_hash)

    epd = epd.EPD()
    _LOGGER.info("Init and clear screen")
    epd.init()
    epd.Clear()

    epd.display(epd.getbuffer(image))
    time.sleep(3)

    logging.info("Refresh done, enter sleep")
    epd.sleep()

    if done_pin:
        enable_done_pin(done_pin)


def load_image_from_path(path: str) -> Image.Image:
    """Load an image from path on disk."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"No file found at: {path}")
    try:
        return Image.open(path)
    except OSError as e:
        _LOGGER.warning(e)
        raise ReferenceError(f"Could not load image from disk at: {path}") from e


def load_image_from_url(url: str, headers: list[str] = []) -> Image.Image:
    """Load an image from url."""
    # Convert headers list into a dictionary
    headers_dict = {
        header.split(":")[0].strip(): header.split(":")[1].strip() for header in headers
    }

    # Make an HTTP GET request to fetch the image
    response = requests.get(url, headers=headers_dict)
    try:
        response.raise_for_status()  # Raise an error for bad HTTP responses
    except requests.ConnectionError as e:
        _LOGGER.warning("No internet connection or URL is unreachable: %s", url)
        raise ReferenceError(
            f"Unable to connect to {url}. Check your internet connection."
        ) from e
    except requests.HTTPError as e:
        _LOGGER.warning("HTTP error occurred: %s", str(e))
        raise ReferenceError(
            f"Could not load image from url at: {url} with headers: {headers}"
        ) from e
    except requests.Timeout as e:
        _LOGGER.warning("Request timed out for URL: %s", url)
        raise ReferenceError(f"Timed out while trying to fetch {url}.") from e

    # Read the image content into a BytesIO object
    image_data = BytesIO(response.content)

    # Open the image using PIL
    image = Image.open(image_data)

    return image


def enable_done_pin(pin: int) -> None:
    """Enable the done pin."""
    if not (9 <= pin <= 27):
        raise ValueError(f"Pin number {pin} must be between 9 and 27.")

    # Initialize the pin as an output device
    done_pin = OutputDevice(pin)

    # Turn on the pin (simulate "done" signal)
    _LOGGER.info("Enable done %d", pin)
    done_pin.on()
    # If using hard-shutdown, the script should stop here as the host loses power
    _LOGGER.info("Done pin %s enabled, waiting 30s for power loss", pin)

    # Let the outside logic handle it, then return
    time.sleep(30)
