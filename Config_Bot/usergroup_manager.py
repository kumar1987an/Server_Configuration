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

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


class Usergroup(object):

    @staticmethod
    def usergroup_add(passwd_entry, group_entry, shadow_entry):

        FileEdit.append_lineaware_mode(
            "/etc/passwd", passwd_entry, "up")
        FileEdit.append_lineaware_mode(
            "/etc/group", group_entry, "up")
        FileEdit.append_lineaware_mode(
            "/etc/shadow", shadow_entry)

    @staticmethod
    def backupfile():
        # For Copying required file for User/Group change related operations
        logger.info(" ---------- File backup started ----------")
        Filecopy.backup("/etc/passwd")
        Filecopy.backup("/etc/group")
        Filecopy.backup("/etc/shadow", Type="secured")
        logger.info(" ---------- File backup Completed ----------")
