""" 
    Codename: file_copy.py

    Author: Kumaran Ramalingam 

    Second Parent Codename: server_config_bot.py

    First Parent Codename: do_main.py
"""

from subprocess import PIPE, Popen
import logging
from datetime import datetime as dt
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


class Filecopy:
    @staticmethod
    def cp(file):

        current_time: str = dt.now().strftime("%d-%m-%y_%H:%M:%S")

        new_file_name: str = "".join((file + "_", current_time))

        Popen(f"sudo cp -ip {file} {new_file_name}".split(), stdout=PIPE, stderr=PIPE)

        Popen(f"cp {file} /tmp/{file}".split(), stdout=PIPE, stderr=PIPE)

        logger.info(f"New backup file created -> {new_file_name}")
