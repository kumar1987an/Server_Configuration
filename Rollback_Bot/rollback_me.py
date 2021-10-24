"""
    Codename: rollback_me.py

    Author: Kumaran Ramalingam

    Description: This Bot act as a main program to call Server configuration
    rollback Bot with various functionalities

"""

# Importing Libraries

import logging
from argparse import ArgumentParser

# from os import access
from rollback_config import RollBackBot


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
    help_doc = """Adhoc requests are fs, ng, ug, sw, cr, pk and all -->
                  fs = filesystems, ng = netgroups,
                  ug = users_groups, sw = softwares,
                  cr = cronusers, pk = pubkeys,
                  all = all categories
               """
    parser.add_argument("--adhoc",
                        type=str,
                        required=True,
                        help=help_doc,
                        nargs="+")

    arg = parser.parse_args()
    return arg.__dict__.get("user"), arg.__dict__.get("adhoc")


if __name__ == "__main__":
    ARGUMENT_EXTRACTED = app()
    print(ARGUMENT_EXTRACTED)
    # SWITCH_ON = RollBackBot(ARGUMENT_EXTRACTED)
    # SWITCH_ON.execute()
