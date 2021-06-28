"""
    Codename: server_config_bot.py

    Author: Kumaran Ramalingam

    Parent Codename:  do_main.py
"""

# Importing Libraries

import json
import logging
import os

# Other files importing

from file_copy import Filecopy
from file_edit import FileEdit
from pubkey_manager import Pubkey
from filesystem_manager import Filesystem

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


class Execute_bot:
    def __init__(self, user):
        self.user = user

    def execute(self):
        """A Bot to perform server configuration with json input"""

        path = "/dummyfs/%s" % self.user

        # This segment of code is for filesystem related executions on requested server
        # ===================================================

        try:

            with open(
                os.path.join(path, "filesystems.json")
            ) as json_file:  # opening json file to read its contents and save into a variable
                json_loader = json.loads(json_file.read())

            # For taking backup file related to LVM
            logger.info(" ---------- File backup started ----------")
            Filecopy.backup("/etc/fstab")
            logger.info(" ---------- File backup Completed ----------")

            logger.debug(" Scanning for newly added disks")
            # Filesystem().disk_scan()  # Calling Disk Scan Method
            logger.debug(" Scan Complete for disks")

            for i in range(len(json_loader)):
                if json_loader[i]["Server"] == os.uname()[1]:
                    fs_type = json_loader[i]["Filesystem"]
                    mount_name = json_loader[i]["Mountpoint"]
                    mount_size = json_loader[i]["Size(G or M)"]
                    mount_owner = json_loader[i]["Owner"]
                    mount_group = json_loader[i]["Group"]
                    mount_perm = json_loader[i]["Permission"]

                    Filesystem().lvm_operation(
                        fs_type, mount_name, mount_size, mount_group, mount_perm)

        except Exception as e:
            print(e)

        # ===================================================
        # This segment of code is for netgroup related executions on requested server

        try:

            with open(
                os.path.join(path, "netgroups.json")
            ) as json_file:  # opening json file to read its contents and save into a variable
                json_loader = json.loads(json_file.read())

            # For Copying required file for Netgroup change related operations
            logger.info(" ---------- File backup started ----------")
            Filecopy.backup("/etc/passwd")
            Filecopy.backup("/etc/nsswitch.conf")
            Filecopy.backup("/etc/group")
            logger.info(" ---------- File backup Completed ----------")

            for i in range(len(json_loader)):
                if json_loader[i]["Server"] == os.uname()[1]:
                    netgroup_name = json_loader[i]["Netgroup"]

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

        except Exception as e:
            print(e)

        # This segment of code is for pubkeys related executions on requested server

        try:

            with open(
                os.path.join(path, "pubkeys.json")
            ) as json_file:  # opening json file to read its contents and save into a variable
                json_loader = json.loads(json_file.read())

            for i in range(len(json_loader)):
                if json_loader[i]["Server"] == os.uname()[1]:
                    user_id = json_loader[i]["userid"]
                    ssh_key = json_loader[i]["ssh-key"]

                    Pubkey.authorized_keys(user_id, ssh_key)
                    logger.info(
                        " PUBKEY REQUEST FOR USER %s COMPLETED" % user_id)

        except Exception as e:
            print(e)

        # This segment of code is for pubkeys related executions on requested server

        try:

            with open(
                os.path.join(path, "usergroups.json")
            ) as json_file:  # opening json file to read its contents and save into a variable
                json_loader = json.loads(json_file.read())

            # For Copying required file for User/Group change related operations
            logger.info(" ---------- File backup started ----------")
            Filecopy.backup("/etc/passwd")
            Filecopy.backup("/etc/group")
            Filecopy.backup("/etc/shadow", Type="secured")
            logger.info(" ---------- File backup Completed ----------")
            # Filecopy.backup("/etc/shadow")

            for i in range(len(json_loader)):
                if json_loader[i]["Server"] == os.uname()[1]:
                    passwd_entry = json_loader[i]["passwd_entry"]
                    group_entry = json_loader[i]["group_entry"]
                    shadow_entry = json_loader[i]["shadow_entry"]

                    FileEdit.append_lineaware_mode(
                        "/etc/passwd", passwd_entry, "up")
                    FileEdit.append_lineaware_mode(
                        "/etc/group", group_entry, "up")
                    FileEdit.append_lineaware_mode(
                        "/etc/shadow", shadow_entry)

        except Exception as e:
            print(e)

        # This segment of code is for softwares related executions on requested server

        try:

            with open(
                os.path.join(path, "softwares.json")
            ) as json_file:  # opening json file to read its contents and save into a variable
                json_loader = json.loads(json_file.read())

        except Exception as e:
            print(e)

        # This segment of code is for cronusers related executions on requested server

        try:

            with open(
                os.path.join(path, "cronusers.json")
            ) as json_file:  # opening json file to read its contents and save into a variable
                json_loader = json.loads(json_file.read())

            # For Copying required file for Netgroup change related operations
            logger.info(" ---------- File backup started ----------")
            Filecopy.backup("/etc/cron.allow")
            logger.info(" ---------- File backup Completed ----------")

            for i in range(len(json_loader)):
                if json_loader[i]["Server"] == os.uname()[1]:
                    cron_user_name = json_loader[i]["User account"]

                    FileEdit.append_mode("/etc/cron.allow", cron_user_name)
                    logger.info(
                        " %s USER HAS BEEN ALLOWED FOR CRONTAB EDIT" % cron_user_name
                    )

        except Exception as e:
            print(e)
