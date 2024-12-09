"""Main entry of the package."""
#!/usr/bin/python

# Configure the root logger
import logging
import os
import sys

from dotenv import load_dotenv

from . import refresh_client

logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level (DEBUG, INFO, WARNING, etc.)
    format="%(asctime)s [%(levelname)8s] %(name)s:%(lineno)s %(message)s",  # Format of the log messages
    handlers=[  # Specify the handlers for the logger
        logging.StreamHandler(sys.stdout)  # Output to stdout
    ],
)


def load_env_vars() -> dict[str, str]:
    """Load environment variables and display the results."""
    load_dotenv()

    env_vars = {}
    for var in ["PIC_PATH", "PIC_URL", "PIC_URL_HEADER", "DONE_PIN"]:
        value = os.getenv(var)
        env_vars[var] = value

    print("\nLoaded environment variables:")
    for var, value in env_vars.items():
        print(f"{var}: {value}")

    return env_vars


if __name__ == "__main__":
    logging.info("Loading parameters from .env and run as package from __main__.py")

    env_vars = load_env_vars()

    refresh_client(
        env_vars.get("PIC_PATH"),
        env_vars.get("PIC_URL"),
        [env_vars["PIC_URL_HEADER"]] if env_vars.get("PIC_URL_HEADER") else [],
        int(env_vars["DONE_PIN"]) if env_vars.get("DONE_PIN") else None,
    )

    logging.info("Exiting...")
