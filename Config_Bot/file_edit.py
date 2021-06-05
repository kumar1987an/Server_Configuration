"""
    Codename: file_edit.py

    Author: Kumaran Ramalingam

    Second Parent Codename: server_config_bot.py

    First Parent Codename:  do_main.py
"""

import logging
import re

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


class FileEdit:
    """this class is to edit file (Dynamic)"""

    @staticmethod
    def append_mode(file, data):
        with open(file, "a") as a_file:
            a_file.writelines(f"+@{data}:x:::::\n")
        logger.info("'%s' --> appended to the file %s" % (data, file))

    @staticmethod
    def find_replace(file, search_pattern, replace_pattern):
        with open(file, "r") as r_file, open(file, "w") as w_file:
            content = r_file.read()
            # w_file.write()

    @staticmethod
    def find_remove():
        return " "

    @staticmethod
    def append_anywhere_mode():
        return " "
