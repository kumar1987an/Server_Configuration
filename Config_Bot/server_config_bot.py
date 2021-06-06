""" 
    Codename: server_config_bot.py

    Author: Kumaran Ramalingam 

    Parent Codename:  do_main.py
"""

# Importing Libraries

import json
import logging
import os
from datetime import datetime as dt
from subprocess import PIPE, Popen, run

from file_copy import Filecopy
from file_edit import FileEdit

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


class Execute_bot:
    def __init__(self, user):
        self.user = user

    def start(self):
        """A Bot to perform server configuration with json input"""

        path: str = f"/dummyfs/{self.user}"

        # This segment of code is for filesystem related executions on requested server

        if os.path.lexists(os.path.join(path, "filesystems.json")):
            pass

        # This segment of code is for netgroup related executions on requested server

        if os.path.lexists(
            os.path.join(path, "netgroups.json")
        ):  # checking for file existence

            with open(
                os.path.join(path, "netgroups.json")
            ) as json_file:  # opening json file to read its contents and save into a variable
                json_loader = json.loads(json_file.read())

            for i in range(len(json_loader)):
                if json_loader[i]["Server"] == os.uname().nodename:
                    netgroup_name = json_loader[i]["Netgroup"]

            # For Copying required file for Netgroup change related operations
            Filecopy.backup("/etc/passwd")
            Filecopy.backup("/etc/nsswitch.conf")
            Filecopy.backup("/etc/group")
            Filecopy.backup("/etc/shadow")

            # Delicate file edit based on actual configuration requirement
            FileEdit.append_mode("/etc/passwd", netgroup_name)
            FileEdit.append_mode("/etc/group", "+:::")

            search_patterns = ["passwd:.+", "group:.+", "shadow:.+", "netgroup:.+"]
            replace_patterns = [
                "passwd:    files sssd",
                "group:    files nis sssd",
                "shadow:    compat",
                "netgroup:    files nis nisplus",
            ]
            FileEdit.find_replace(
                "/tmp/nsswitch.conf", search_patterns, replace_patterns
            )
            Filecopy.copy_file("/tmp/nsswitch.conf", "/etc/nsswitch_conf")

        # This segment of code is for pubkeys related executions on requested server

        if os.path.lexists(os.path.join(path, "pubkeys.json")):
            pass

        # This segment of code is for pubkeys related executions on requested server

        if os.path.lexists(os.path.join(path, "user_groups.json")):
            pass

        # This segment of code is for softwares related executions on requested server

        if os.path.lexists(os.path.join(path, "softwares.json")):
            pass

        # This segment of code is for cronusers related executions on requested server

        if os.path.lexists(os.path.join(path, "cronusers.json")):
            pass
