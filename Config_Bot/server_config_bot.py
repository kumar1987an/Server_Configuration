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
from cronuser_manager import Cron
from software_manager import SoftwareManager

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

        # This segment of code is for user groups related executions on requested server

        try:

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
                        passwd_entry, group_entry, shadow_entry
                    )

        except Exception as e:
            print(e)

        # This segment of code is for netgroup related executions on requested server

        try:

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

        # This segment of code is for software related executions on requested server

        try:

            with open(
                os.path.join(path, "softwares.json")
            ) as json_file:  # opening json file to read its contents and save into a variable
                json_loader = json.loads(json_file.read())
            for i in range(len(json_loader)):
                pass

        except Exception as e:
            print(e)

        # This segment of code is for filesystem related executions on requested servers

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

            (
                percentage_used,
                filesystem_used,
                lv_vg_pv_used,
            ) = Filesystem.lvm_full_scan_template()

            if filesystem_used:

                mount_names = [
                    json_loader[i]["Mountpoint"]
                    for i in range(len(json_loader))
                    if json_loader[i]["Server"] == os.uname()[1]
                ]
                filesystems_to_be_removed = [
                    fs for fs in filesystem_used if fs not in mount_names
                ]

                filesystems_to_be_created = [
                    mount_name
                    for mount_name in mount_names
                    if mount_name not in filesystem_used
                ]
                if filesystems_to_be_removed:
                    Filesystem.check_and_wipe_out_lvm(
                        percentage_used, filesystems_to_be_removed, lv_vg_pv_used
                    )

                elif filesystems_to_be_created:
                    for i in filesystems_to_be_created:
                        for j in json_loader:
                            if j["Mountpoint"] == i:
                                fs_type = j["Filesystem"]
                                mount_name = j["Mountpoint"]
                                mount_size = j["Size(only in G)"]
                                mount_owner = j["Owner"]
                                mount_group = j["Group"]
                                mount_perm = j["Permission"]
                                print(
                                    fs_type,
                                    mount_name,
                                    mount_size,
                                    mount_owner,
                                    mount_group,
                                    mount_perm,
                                )
                                Filesystem.lvm_operation(
                                    fs_type,
                                    mount_name,
                                    mount_size,
                                    mount_owner,
                                    mount_group,
                                    int(mount_perm),
                                )
                else:
                    logger.info(
                        " No filesystems are required to be removed as filesystems already exists"
                    )

            elif lv_vg_pv_used:
                for metadata in lv_vg_pv_used:
                    lv = metadata.split()[0]
                    vg = metadata.split()[1]
                    pv = metadata.split()[2]
                    logger.warning(
                        "Have a check on existing PV = {}, VG = {} and LV = {}".format(
                            pv, vg, lv
                        )
                    )

            else:
                for i in range(len(json_loader)):
                    if json_loader[i]["Server"] == os.uname()[1]:
                        fs_type = json_loader[i]["Filesystem"]
                        mount_name = json_loader[i]["Mountpoint"]
                        mount_size = json_loader[i]["Size(only in G)"]
                        mount_owner = json_loader[i]["Owner"]
                        mount_group = json_loader[i]["Group"]
                        mount_perm = json_loader[i]["Permission"]
                        # print(fs_type, mount_name, mount_size, mount_owner, mount_group, mount_perm)
                        Filesystem.lvm_operation(
                            fs_type,
                            mount_name,
                            mount_size,
                            mount_owner,
                            mount_group,
                            int(mount_perm),
                        )

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
                    Cron.cron_useradd(cron_user_name)

        except Exception as e:
            print(e)
