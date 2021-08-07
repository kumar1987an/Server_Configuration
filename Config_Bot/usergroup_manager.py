"""
    Codename: usergroup_manager.py

    Author: Kumaran Ramalingam

    Parent Codename:  server_config_bot.py
"""

# Importing Libraries
import logging
import os

# Other files importing
from file_copy import Filecopy
from file_edit import FileEdit
from checker import Duplicate

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


class Usergroup(object):

    @staticmethod
    def netgroup_with_usergroup_add(passwd_entry, group_entry, shadow_entry):

        if Duplicate.single_pattern_file_checker(passwd_entry, "/etc/passwd") == 1:
            FileEdit.append_lineaware_mode(
                "/etc/passwd", passwd_entry, "up")
        else:
            logger.warning(
                " Configuration entry already exists in passwd file")

        if Duplicate.single_pattern_file_checker(group_entry, "/etc/group") == 1:
            FileEdit.append_lineaware_mode(
                "/etc/group", group_entry, "up")
        else:
            logger.warning(" Configuration entry already exists in group file")

        if Duplicate.single_pattern_file_checker(shadow_entry, "/etc/shadow") == 1:
            FileEdit.append_lineaware_mode(
                "/etc/shadow", shadow_entry)
        else:
            logger.warning(
                " Configuration entry already exists in shadow file")

    @staticmethod
    def only_usergroup_add(passwd_entry, group_entry, shadow_entry):

        if Duplicate.single_pattern_file_checker(passwd_entry, "/etc/passwd") == 1:
            FileEdit.normal_append_mode("/etc/passwd", passwd_entry)
        else:
            logger.warning(
                " Configuration entry already exists in passwd file")

        if Duplicate.single_pattern_file_checker(passwd_entry, "/etc/passwd") == 1:
            FileEdit.normal_append_mode("/etc/group", group_entry)
        else:
            logger.warning(" Configuration entry already exists in group file")

        if Duplicate.single_pattern_file_checker(passwd_entry, "/etc/passwd") == 1:
            FileEdit.normal_append_mode("/etc/shadow", shadow_entry)
        else:
            logger.warning(
                " Configuration entry already exists in shadow file")

    @staticmethod
    def backupfile():
        # For Copying required file for User/Group change related operations
        logger.info(" ---------- File backup started ----------")
        Filecopy.backup("/etc/passwd", for_what_backup="usergroup")
        Filecopy.backup("/etc/group", for_what_backup="usergroup")
        Filecopy.backup("/etc/shadow", type_of_bkp="secured")
        logger.info(" ---------- File backup Completed ----------")
