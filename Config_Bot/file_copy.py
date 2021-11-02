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


class Filecopy(object):

    @staticmethod
    def backup(file_name, for_what_backup="backup", type_of_bkp="normal"):
        """Function definition: To backup of a file"""

        current_time = for_what_backup + "_" + dt.now().strftime(r"%d-%m-%y_%H:%M:%S")

        new_file_name = "".join((file_name + "_", current_time))

        if type_of_bkp == "normal":
            Popen(
                "cp -p {} {}".format(file_name, new_file_name).split(),
                stdout=PIPE,
                stderr=PIPE,
            )
            logger.info(
                " Primary backup file created -> {}".format(new_file_name))
            Popen(
                "cp -p {} /tmp/{}".format(file_name,
                                          os.path.basename(file_name)).split(),
                stdout=PIPE,
                stderr=PIPE,
            )
            logger.info(" Secondary backup file created -> /tmp/{}".format(
                os.path.basename(file_name))
            )
        elif type_of_bkp == "secured":
            Popen(
                "cp -p {} {}".format(file_name, new_file_name).split(),
                stdout=PIPE,
                stderr=PIPE,
            )
            logger.info(" Primary backup file for {} created and new \
                        file name secured".format(os.path.basename(file_name)))

    @ staticmethod
    def copy_file(source_file, target_file):
        """Function definiton: To copy a file"""

        command = "cp -p {} {}".format(source_file, target_file).split()
        Popen(command, stdout=PIPE, stderr=PIPE)

        logger.info(" {} has been copied to {}".format(
            source_file, target_file))
