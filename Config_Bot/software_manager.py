"""
    Codename: software.py

    Author: Kumaran Ramalingam

    Second Parent Codename: server_config_bot.py

    First Parent Codename:  main.py
"""

import os
import logging
import platform
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
        kernel = platform.uname()[2]
        system_flavor, system_version = platform.platform().split(
            "-")[5], platform.platform().split("-")[6]
        return kernel, system_flavor, system_version

    @staticmethod
    def load_repo():
        kernel, system_flavor, system_version = SoftwareManager.arch_check()
        return kernel, system_version, system_flavor

    @staticmethod
    def install_software(software_name):
        pass

    @staticmethod
    def deinstall_software(software_name):
        pass

    @staticmethod
    def software_check(software_name):
        pass


print(SoftwareManager.load_repo())
