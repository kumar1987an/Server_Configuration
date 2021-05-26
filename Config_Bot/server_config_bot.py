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

            Filecopy.cp("/etc/passwd")
            Filecopy.cp("/etc/nsswitch.conf")
            Filecopy.cp("/etc/group")
            Filecopy.cp("/etc/shadow")

            FileEdit.append("/etc/passwd", netgroup_name)
            FileEdit.append("/etc/group", "+:::")

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
