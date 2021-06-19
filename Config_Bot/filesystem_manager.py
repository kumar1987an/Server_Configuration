"""
    Codename: filesystem_manager.py

    Author: Kumaran Ramalingam

    Second Parent Codename: server_config_bot.py

    First Parent Codename:  main.py
"""

import os
import logging
from subprocess import check_output, Popen, PIPE, call

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
    def fs_backup(filesystems):  # filesystems input as list of filesytems to be backuped
        if filesystems:
            for fs in filesystems:
                dirname = fs.split("/")[1]
                Popen(r"tar -cvf /var/tmp/{}.tar /{}".format(dirname,
                                                             dirname).split(), stdout=PIPE, stderr=PIPE)
                tar_check = call(
                    r"ls /var/tmp/{}.tar".format(dirname).split(), stdout=PIPE, stderr=PIPE)
                return tar_check

    @staticmethod
    def fs_scan():
        """ This function will take care of new disk scan to 
        the server and also will take backups if necessary of required filesytems """
        command1 = r"df -h | egrep -v 'root|dxc|mnt|swap|snap|udev|sd|tmpfs|boot'|tail -n +2 | awk -F' ' '{print $5}'"
        command2 = r"df -h | egrep -v 'root|dxc|mnt|swap|snap|udev|sd|tmpfs|boot'|tail -n +2 | awk -F' ' '{print $NF}'"
        percentage_used = check_output(command1, shell=True).decode().split()
        filesys_name = check_output(command2, shell=True).decode().split()
        unused_filesystems = []
        for percent, filesys in zip(percentage_used, filesys_name):
            if percent in ["1%", "2%", "3%", "4%", "5%"]:
                unused_filesystems.append(filesys)
            else:
                logger.critical(
                    "{} is more than 5% occupied please perform \
                        FS backup manually and re-run the program".format(filesys))
        return unused_filesystems

    @staticmethod
    def lvm_oper():
        return Filesystem.fs_scan()
