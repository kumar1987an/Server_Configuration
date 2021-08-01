"""
    Codename: checker.py

    Author: Kumaran Ramalingam

    Second Parent Codename: server_config_bot.py

    First Parent Codename:  main.py
"""

import os
import logging
from subprocess import PIPE, call, Popen

# Importing required libraries
from file_edit import FileEdit
from checker import Duplicate

# Other files importing

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


class Cron(object):

    @staticmethod
    def cron_useradd(cron_user_name):
        if Duplicate.single_pattern_file_checker(cron_user_name, "/etc/cron.allow") == 1:
            FileEdit.normal_append_mode("/etc/cron.allow", cron_user_name)
            logger.info(" %s USER HAS BEEN ALLOWED FOR CRONTAB EDIT" %
                        cron_user_name)
        else:
            logger.warning(
                "Cron user {} already exists in config file".format(cron_user_name))
