"""
    Codename: checker.py

    Author: Kumaran Ramalingam

    Second Parent Codename: server_config_bot.py

    First Parent Codename:  main.py
"""

# import os
import logging
import re

# from subprocess import PIPE, call, Popen

# Importing required libraries

# Other files importing

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


class Duplicate(object):
    """Checking for ducplication of configuration on a file"""

    @staticmethod
    def single_pattern_file_checker(single_pattern, file):
        """Single pattern file checker"""
        check_for = re.compile("{}".format(single_pattern))
        with open(file, "r") as check_file:
            file_data = check_file.read()
            pattern_check = re.search(check_for, file_data)
            if pattern_check is None:
                return 1  # Execute the Script
            else:
                return 0  # Don't Execute the Script

    @staticmethod
    def multi_pattern_file_checker(multi_pattern, file):
        """Multiple pattern file checker"""
        list_of_pattern_verified = []
        for pattern in multi_pattern:
            check_for = re.compile("{}".format(pattern))
            with open(file, "r") as check_file:
                file_data = check_file.read()
                pattern_check = re.search(check_for, file_data)
                if pattern_check is None:
                    list_of_pattern_verified.append(True)  # Execute the Script
                else:
                    list_of_pattern_verified.append(
                        False)  # Don't Execute the Script

        if all(list_of_pattern_verified):
            return 1  # Execute the Script
        else:
            return 0  # Don't Execute the Script
