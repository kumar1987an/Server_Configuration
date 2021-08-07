"""
    Codename: pubkey_manager.py

    Author: Kumaran Ramalingam

    Second Parent Codename: server_config_bot.py

    First Parent Codename:  main.py
"""

# Importing required libraries
import os
import logging

# Other files importing
from file_copy import Filecopy

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


class Pubkey(object):

    @staticmethod
    def path_finder(user):

        if os.path.lexists("/SSH_Keys/{}".format(user)):
            return 0
        else:
            return 1

    @staticmethod
    def path_creator(user):

        logger.warning(
            " Pubkey store directory for user {} doesn't exist, creating it now".format(user))
        os.makedirs("/SSH_Keys/{}".format(user))
        if os.path.lexists("/SSH_Keys"):
            logger.info(
                " Pubkey store directory for user {} created Success".format(user))

    @staticmethod
    def authorized_keys(user, pub_key):

        if Pubkey.path_finder(user) == 0:
            path = "/SSH_Keys/{}".format(user)
            authorized_file = os.path.join(path, "authorized_keys2")
            Filecopy.backup("{}".format(authorized_file), type_of_bkp="secured")
            try:
                with open(authorized_file, "a") as key_file:
                    key_file.write("{}\n".format(pub_key))
                logger.info(
                    " Updated authorization file for user {}".format(user))

            except Exception as e:
                print(e)

        elif Pubkey.path_finder(user) == 1:
            Pubkey.path_creator(user)
            Pubkey.authorized_keys(user, pub_key)
