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
        logger.debug(" Proceeding system wide disk scan")
        ps1 = Popen("ls /sys/class/scsi_host/".split(), stdout=PIPE)
        for i in ps1.communicate()[0].decode().split():
            try:
                os.system(
                    "echo '- - -' > /sys/class/scsi_host/{}/scan".format(i))

            except Exception as e:
                print(e)
        logger.debug(" System wide Disk Scan Completed successfully")

    @staticmethod
    def fs_backup(filesystem):  # filesystems input as list of filesytems to be backuped
        logger.info(" Filesystem {} backup Started".format(filesystem))
        dirname = filesystem.split("/")[1]
        Popen(r"tar -cvf /var/tmp/{}.tar /{}".format(dirname,
                                                     dirname).split(), stdout=PIPE, stderr=PIPE)
        tar_check = call(
            r"ls /var/tmp/{}.tar".format(dirname).split(), stdout=PIPE, stderr=PIPE)
        if tar_check == 0:
            logger.info(" Filesystem {} backup completed".format(dirname))

        else:
            logger.critical(
                " Filesystem backup not happened please login to the system and verified")

    @staticmethod
    def fs_scan():
        """ This function will take care of new disk scan to 
        the server and also will take backups if necessary of required filesytems """
        logger.info(" Proceeding with PV, VG, LV and FS scan")
        Filesystem.disk_scan()  # Calling Disk Scan Method
        command1 = r"df -h | egrep -v 'root|dxc|mnt|swap|snap|udev|sd|tmpfs|boot'|tail -n +2 | awk -F' ' '{print $5}'"
        command2 = r"df -h | egrep -v 'root|dxc|mnt|swap|snap|udev|sd|tmpfs|boot'|tail -n +2 | awk -F' ' '{print $NF}'"
        percentage_used = check_output(command1, shell=True).decode().split()
        filesys_name = check_output(command2, shell=True).decode().split()
        unused_filesystems = []
        if percentage_used and filesys_name:
            for percent, filesys in zip(percentage_used, filesys_name):
                if percent in ["1%", "2%", "3%", "4%", "5%"]:
                    Filesystem.fs_backup(filesys)
                else:
                    logger.critical("{} is more than 5% occupied please perform \
                        FS backup manually and re-run the program".format(filesys))
            logger.info(" PV, VG, LV and FS scan successfully completed")
        else:
            logger.info(
                " There are no existing app releated filesytem available")

    @staticmethod
    def lvm_oper():
        logger.info(" LVM Operation Started")
        Filesystem.fs_scan()
