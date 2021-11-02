"""
    Codename: do_main.py

    Author: Kumaran Ramalingam

    Description: This Bot act as a main program to call Server
    configuration Bot with various functionalities
"""

# Importing Libraries

from argparse import ArgumentParser
import logging
from server_config_bot import ExecuteBot


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

FORMATTER = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")

STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setFormatter(FORMATTER)

LOGGER.addHandler(STREAM_HANDLER)


def app():
    """Argument parser"""
    parser = ArgumentParser()
    parser.add_argument(
        "--user",
        type=str,
        required=True,
        help="Enter the username for location to save the jsons",
    )

    arg = parser.parse_args()
    return arg.__dict__.get("user")


if __name__ == "__main__":
    ARGUMENT_EXTRACTOR = app()
    SWITCH_ON = ExecuteBot(ARGUMENT_EXTRACTOR)
    SWITCH_ON.execute()
