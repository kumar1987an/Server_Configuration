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
    def backup(file):
        """Function definiton: To backup of a file"""

        current_time: str = dt.now().strftime("%d-%m-%y_%H:%M:%S")

        new_file_name: str = "".join((file + "_", current_time))

        Popen(f"sudo cp -ip {file} {new_file_name}".split(), stdout=PIPE, stderr=PIPE)

        Popen(
            f"cp {file} /tmp/{os.path.basename(file)}".split(), stdout=PIPE, stderr=PIPE
        )

        logger.info(f"New backup file created -> {new_file_name}")
        logger.info(f"Secondar backup file created -> /tmp/{os.path.basename(file)}")

    @staticmethod
    def copy_file(source_file, target_file):
        """Function definiton: To copy a file"""

        command = f"cp -ip {source_file} {target_file}".split()
        Popen(command, stdout=PIPE, stderr=PIPE)

        logger.info(f"{source_file} has been copied to {target_file}")
