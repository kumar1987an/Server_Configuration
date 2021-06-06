"""
    Codename: file_edit.py

    Author: Kumaran Ramalingam

    Second Parent Codename: server_config_bot.py

    First Parent Codename:  do_main.py
"""

import logging
import re
import os

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
        """Function definition: for appending data to a file"""

        if os.path.basename(file) == "passwd":
            with open(file, "a") as a_file:
                a_file.writelines(f"+@{data}:x:::::\n")

        elif os.path.basename(file) == "group":
            with open(file, "a") as a_file:
                a_file.writelines("+:::\n")

        else:
            with open(file, "a") as a_file:
                a_file.writelines(data)

        logger.info("'%s' --> appended to the file %s" % (data, file))

    @staticmethod
    def find_replace(file, search_pattern, replace_pattern):
        """Function definition: for find and replace data to a file"""

        for s_pattern, r_pattern in zip(search_pattern, replace_pattern):

            if os.path.basename(file) == "nsswitch.conf":

                with open(file, "r") as in_file:
                    content = in_file.read()

                if s_pattern == "passwd:.+":
                    output_content = re.sub(s_pattern, r_pattern, content)

                elif s_pattern == "group:.+":
                    output_content = re.sub(s_pattern, r_pattern, content)

                elif s_pattern == "shadow:.+":
                    output_content = re.sub(s_pattern, r_pattern, content, count=1)

                else:
                    output_content = re.sub(s_pattern, r_pattern, content)

                with open(file, "w") as out_file:
                    out_file.write(output_content)
            else:
                pass  # Need to add codes if further files to be edited based on situation

    @staticmethod
    def find_remove():
        return " "

    @staticmethod
    def append_anywhere_mode():
        return " "
