"""
    Codename: rollback_config.py

    Author: Kumaran Ramalingam

    Parent Codename:  rollback_me.py
"""

# Importing Libraries
import json
import logging
import os

# Other files importing

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

FORMATTER = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")

STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setFormatter(FORMATTER)

LOGGER.addHandler(STREAM_HANDLER)


class RollBackBot:
    """ RollBackBot class"""

    def __init__(self, user, adhoc):
        self.user = user
        self.adhoc = adhoc

    def execute(self):
        """A Bot to perform server configuration with json input"""

        path = "/dummyfs/%s" % self.user
        for adhoc in self.adhoc:
            if adhoc == "fs":
                json_file_path = os.path.join(path, "filesystems.json")
                with open(json_file_path, "r") as json_file:
                    json_loader = json.loads(json_file.read())
                    for data in json_loader:
                        if data['Server'] == os.uname()[1]:
                            print(data)

            if adhoc == "ug":
                json_file_path = os.path.join(path, "usergroups.json")
                with open(json_file_path, "r") as json_file:
                    json_loader = json.loads(json_file.read())
                    for data in json_loader:
                        if data['Server'] == os.uname()[1]:
                            print(data)

            if adhoc == "pk":
                json_file_path = os.path.join(path, "pubkeys.json")
                with open(json_file_path, "r") as json_file:
                    json_loader = json.loads(json_file.read())
                    for data in json_loader:
                        if data['Server'] == os.uname()[1]:
                            print(data)

            if adhoc == "ng":
                json_file_path = os.path.join(path, "netgroups.json")
                with open(json_file_path, "r") as json_file:
                    json_loader = json.loads(json_file.read())
                    for data in json_loader:
                        if data['Server'] == os.uname()[1]:
                            print(data)

            if adhoc == "sw":
                json_file_path = os.path.join(path, "softwares.json")
                with open(json_file_path, "r") as json_file:
                    json_loader = json.loads(json_file.read())
                    for data in json_loader:
                        if data['Server'] == os.uname()[1]:
                            print(data)

            if adhoc == "cr":
                json_file_path = os.path.join(path, "cronusers.json")
                with open(json_file_path, "r") as json_file:
                    json_loader = json.loads(json_file.read())
                    for data in json_loader:
                        if data['Server'] == os.uname()[1]:
                            print(data)
