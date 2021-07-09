"""
    Codename: netgroup_manager.py

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


class Netgroup(object):

    @staticmethod
    def netgroup_add(netgroup_name):

        # Delicate file edit based on actual configuration requirement
        FileEdit.append_mode("/etc/passwd", netgroup_name)
        FileEdit.append_mode("/etc/group", "+:::")

        search_patterns = [
            "passwd:.+",
            "group:.+",
            "shadow:.+",
            "netgroup:.+",
        ]
        replace_patterns = [
            "passwd:    files sssd",
            "group:    files nis sssd",
            "shadow:    compat",
            "netgroup:    files nis nisplus",
        ]

        FileEdit.find_replace(
            "/tmp/nsswitch.conf", search_patterns, replace_patterns
        )

        Filecopy.copy_file("/tmp/nsswitch.conf",
                           "/etc/nsswitch.conf")
        logger.info(" %s NETGROUP REQUEST COMPLETED" %
                    netgroup_name)

    @staticmethod
    def backupfile():
        # For Copying required file for Netgroup change related operations
        logger.info(" ---------- File backup started ----------")
        Filecopy.backup("/etc/passwd")
        Filecopy.backup("/etc/nsswitch.conf")
        Filecopy.backup("/etc/group")
        logger.info(" ---------- File backup Completed ----------")
