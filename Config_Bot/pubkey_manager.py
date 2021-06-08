"""
    Codename: pubkey_manager.py

    Author: Kumaran Ramalingam

    Second Parent Codename: server_config_bot.py

    First Parent Codename:  main.py
"""

from file_copy import Filecopy
import hashlib
import os
from subprocess import PIPE, Popen
import logging

# Importing required libraries

# Other files importing

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


class Pubkey:

    @staticmethod
    def path_finder(user):

        if os.path.lexists("/SSH_Keys/{}".format(user)):
            return 0
        else:
            return 1

    @staticmethod
    def path_creator(user):

        print(
            "pubkey store directory for user {} doesn't exist, creating it now".format(user))
        os.makedirs("/SSH_Keys/{}".format(user))
        if os.path.lexists("/SSH_Keys"):
            print(
                "pubkey store directory for user {} created printing output".format(user))
        ps1 = Popen("ls -ld /SSH_Keys/{}".format(user).split(),
                    stdout=PIPE, stderr=PIPE)
        return ps1.communicate()[0]

    @staticmethod
    def hash_checker(file):
        md5_hash = hashlib.md5()
        with open(file, "rb") as hash_file:
            content = hash_file.read()
        md5_hash.update(content)
        return md5_hash.hexdigest()

    @staticmethod
    def authorized_keys(user, pub_key):

        if Pubkey.path_finder(user) == 0:
            path = "/SSH_Keys/{}".format(user)
            authorized_file = os.path.join(path, "authorized_keys2")
            Filecopy.backup("{}".format(authorized_file), Type="secured")
            print(Filecopy.backup.__dict__["new_file_name"])
            try:
                with open(authorized_file, "a") as key_file:
                    key_file.write("{}\n".format(pub_key))
                print("Updated authorization file for user {}".format(user))

            except Exception as e:
                print(e)

        elif Pubkey.path_finder(user) == 1:
            print(Pubkey.path_creator(user))
            Pubkey.authorized_keys(user, pub_key)
