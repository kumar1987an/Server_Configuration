""" 
    Codename: do_main.py

    Author: Kumaran Ramalingam 

    Description: This Bot act as a main program to call Server configuration Bot with various functionalities
"""

# Importing Libraries

from server_config_bot import Execute_bot
from argparse import ArgumentParser
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


def main():
    """ Argument parser """
    parser = ArgumentParser()
    parser.add_argument(
        "--user",
        type=str,
        required=True,
        help="Enter the username for location to save the jsons",
    )

    arg = parser.parse_args()
    Execute_bot.start(arg)


if __name__ == "__main__":
    main()
