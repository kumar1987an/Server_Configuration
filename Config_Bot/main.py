""" 
    Codename: do_main.py

    Author: Kumaran Ramalingam 

    Description: This Bot act as a main program to call Server configuration Bot with various functionalities
"""

# Importing Libraries

from os import access
from server_config_bot import ExecuteBot
from argparse import ArgumentParser
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


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
    argument_extracted = app()
    switch_on = ExecuteBot(argument_extracted)
    switch_on.execute()
