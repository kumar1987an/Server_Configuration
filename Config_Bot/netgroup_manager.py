"""
    Codename: netgroup_manager.py

    Author: Kumaran Ramalingam

    Parent Codename:  server_config_bot.py
"""

# Importing Libraries
import logging

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


class Netgroup(object):

    @staticmethod
    def netgroup_add(netgroup_name):

        # Delicate file edit based on actual configuration requirement
        if Duplicate.single_pattern_file_checker(netgroup_name, "/etc/passwd") == 1:
            FileEdit.with_netgroup_append_mode("/etc/passwd", netgroup_name)
        else:
            logger.warning("Netgroup Entry already there in the passwd file")

        if Duplicate.single_pattern_file_checker("+:::", "/etc/group") == 1:
            FileEdit.with_netgroup_append_mode("/etc/group", "+:::")
        else:
            logger.warning("Netgroup Entry already there in the group file")

        if Duplicate.multi_pattern_file_checker(["passwd.*files.*nis",
                                                "group.*files.*nis",
                                                 "shadow.*compat",
                                                 "netgroup.*files.*nis"], "/etc/nsswitch.conf") == 1:
            search_patterns = [
                "passwd:.+",
                "group:.+",
                "shadow:.+",
                "netgroup:.+",
            ]
            replace_patterns = [
                "passwd:    files nis",
                "group:     files nis",
                "shadow:    compat",
                "netgroup:  files nis",
            ]

            FileEdit.find_replace(
                "/tmp/nsswitch.conf", search_patterns, replace_patterns
            )
            Filecopy.copy_file("/tmp/nsswitch.conf",
                               "/etc/nsswitch.conf")
            logger.info(" %s NETGROUP REQUEST COMPLETED" %
                        netgroup_name)
        else:
            logger.warning(
                "nsswitch.conf file doesnt required a config update")

    @staticmethod
    def backupfile():
        # For Copying required file for Netgroup change related operations
        logger.info(" ---------- File backup started ----------")
        Filecopy.backup("/etc/passwd")
        Filecopy.backup("/etc/nsswitch.conf")
        Filecopy.backup("/etc/group")
        logger.info(" ---------- File backup Completed ----------")
