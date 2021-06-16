"""
    Codename: filesystem_manager.py

    Author: Kumaran Ramalingam

    Second Parent Codename: server_config_bot.py

    First Parent Codename:  main.py
"""

import os
import logging
from subprocess import check_output, Popen, PIPE

# Importing required libraries

# Other files importing

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


class Filesystem:

    @staticmethod
    def disk_scan():
        ps1 = Popen("ls /sys/class/scsi_host/".split(), stdout=PIPE)
        for i in ps1.communicate()[0].decode().split():
            try:
                os.system(
                    "echo '- - -' > /sys/class/scsi_host/{}/scan".format(i))

            except Exception as e:
                print(e)

    @staticmethod
    def lvm_scan():
        command1 = r"df -h | egrep -v 'root|swap|snap|udev|sd|tmpfs|boot'|tail -n +2 | awk -F' ' '{print $5}'"
        command2 = r"df -h | egrep -v 'root|swap|snap|udev|sd|tmpfs|boot'|tail -n +2 | awk -F' ' '{print $NF}'"
        percentage_used = check_output(command1, shell=True).decode().split()
        filesys_name = check_output(command2, shell=True).decode().split()
        unused_filesystems = []
        for percent, filesys in zip(percentage_used, filesys_name):
            if percent == "1%":
                unused_filesystems.append(filesys)
        if unused_filesystems:
            for fs in unused_filesystems:
                print(os.path.basename(fs))

    @staticmethod
    def lvm_backup():
        pass

    @staticmethod
    def lvm_oper():
        pass
