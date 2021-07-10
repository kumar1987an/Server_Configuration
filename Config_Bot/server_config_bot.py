"""
    Codename: server_config_bot.py

    Author: Kumaran Ramalingam

    Parent Codename:  main.py
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
from usergroup_manager import Usergroup
from netgroup_manager import Netgroup

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


class ExecuteBot:

    def __init__(self, user):
        self.user = user

    def execute(self):
        """A Bot to perform server configuration with json input"""

        path = "/dummyfs/%s" % self.user

        files_list = os.listdir(path)

        if "usergroups.json" in files_list:

            # This segment of code is for user groups related executions on requested server

            with open(
                os.path.join(path, "usergroups.json")
            ) as json_file:  # opening json file to read its contents and save into a variable
                json_loader = json.loads(json_file.read())

            # For Copying required file for User/Group change related operations
            Usergroup.backupfile()

            for i in range(len(json_loader)):
                if json_loader[i]["Server"] == os.uname()[1]:
                    passwd_entry = json_loader[i]["passwd_entry"]
                    group_entry = json_loader[i]["group_entry"]
                    shadow_entry = json_loader[i]["shadow_entry"]

                    # Calling usergroup adding execution
                    Usergroup.only_usergroup_add(
                        passwd_entry, group_entry, shadow_entry)

        if "netgroups.json" in files_list:

            # This segment of code is for netgroup related executions on requested server

            with open(
                os.path.join(path, "netgroups.json")
            ) as json_file:  # opening json file to read its contents and save into a variable
                json_loader = json.loads(json_file.read())

            # For Copying required file for Netgroup change related operations
            Netgroup.backupfile()

            for i in range(len(json_loader)):
                if json_loader[i]["Server"] == os.uname()[1]:
                    netgroup_name = json_loader[i]["Netgroup"]

                    # Calling netgroup adding execution
                    Netgroup.netgroup_add(netgroup_name)

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

        # This segment of code is for softwares related executions on requested server

        try:

            with open(
                os.path.join(path, "softwares.json")
            ) as json_file:  # opening json file to read its contents and save into a variable
                json_loader = json.loads(json_file.read())
            for i in range(len(json_loader)):
                pass

        except Exception as e:
            print(e)

        # This segment of code is for filesystem related executions on requested server

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
            # Filesystem.disk_scan()  # Calling Disk Scan Method
            logger.debug(" Scan Complete for disks")

            percentage_used, filesystem_used, lv_vg_pv_used = Filesystem.lvm_full_scan_template()

            if bool(filesystem_used) is True:  # Need to make it back as True after testing
                Filesystem.check_and_wipeoutlvm(
                    percentage_used, filesystem_used, lv_vg_pv_used)

            elif bool(lv_vg_pv_used) is True:  # Need to make it back as True after testing
                Filesystem.check_and_warn(lv_vg_pv_used)

            else:
                for i in range(len(json_loader)):
                    if json_loader[i]["Server"] == os.uname()[1]:
                        fs_type = json_loader[i]["Filesystem"]
                        mount_name = json_loader[i]["Mountpoint"]
                        mount_size = json_loader[i]["Size(only in G)"]
                        mount_owner = json_loader[i]["Owner"]
                        mount_group = json_loader[i]["Group"]
                        mount_perm = json_loader[i]["Permission"]

                        Filesystem.lvm_operation(
                            fs_type, mount_name, mount_size, mount_owner, mount_group, mount_perm)

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

                    FileEdit.normal_append_mode(
                        "/etc/cron.allow", cron_user_name)
                    logger.info(
                        " %s USER HAS BEEN ALLOWED FOR CRONTAB EDIT" % cron_user_name
                    )

        except Exception as e:
            print(e)
