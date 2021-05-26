"""
    Codename: file_edit.py

    Author: Kumaran Ramalingam

    Second Parent Codename: server_config_bot.py

    First Parent Codename:  do_main.py
"""

import logging
import shutil

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


class FileEdit:
    """this class is to edit file (Dynamic)"""

    @staticmethod
    def append(file, data):
        with open(file, "a") as a_file:
            a_file.writelines(f"+@{data}:x:::::\n")
        logger.info(f"'{data}' --> appended to the file {file}")

    @staticmethod
    def edit_mode():
        pass
