"""
    Codename: software.py

    Author: Kumaran Ramalingam

    Second Parent Codename: server_config_bot.py

    First Parent Codename:  main.py
"""

import os
import logging
from subprocess import PIPE, call, Popen

# Importing required libraries

# Other files importing

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


class SoftwareManager(object):
    @staticmethod
    def arch_check():
        for i, j in os.environ.items():
            print(i + ":    " + j)

    @staticmethod
    def load_repo():
        pass

    @staticmethod
    def install_software(software_name):
        pass

    @staticmethod
    def deinstall_software(software_name):
        pass

    @staticmethod
    def software_check(software_name):
        pass


print(SoftwareManager.arch_check())
