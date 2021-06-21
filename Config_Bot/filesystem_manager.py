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
    def fs_scan_template():
        command1 = r"df -h | egrep -v 'root|dxc|mnt|dummy|swap|snap|udev|sd|tmpfs|boot'|tail -n +2 | awk -F' ' '{print $5}'"
        command2 = r"df -h | egrep -v 'root|dxc|mnt|dummy|swap|snap|udev|sd|tmpfs|boot'|tail -n +2 | awk -F' ' '{print $NF}'"
        command3 = r"df -h | egrep -v 'root|dxc|mnt|dummy|swap|snap|udev|sd|tmpfs|boot'|tail -n +2 | awk -F' ' '{print $1}'"
        used_percentage = check_output(command1, shell=True).decode().split()
        used_filesystem = check_output(command2, shell=True).decode().split()
        used_volumegroup = check_output(command3, shell=True).decode().split()
        return used_percentage, used_filesystem, used_volumegroup

    @staticmethod
    def fs_scan():
        """ This function will take care of new disk scan to 
        the server and also will take backups if necessary of required filesytems """
        # Filesystem.disk_scan()  # Calling Disk Scan Method
        percentage_used, filesystem_used, _ = Filesystem.fs_scan_template()
        if bool(percentage_used and filesystem_used) == True:
            logger.info(" Proceeding with PV, VG, LV and FS scan")
            for percent, filesys in zip(percentage_used, filesystem_used):
                if percent in ["1%", "2%", "3%", "4%", "5%"]:
                    Filesystem.fs_backup(filesys)
                else:
                    logger.critical("{} is more than 5% occupied please perform \
                        FS backup manually and re-run the program".format(filesys))
            logger.info(" PV, VG, LV and FS scan successfully completed")
        else:
            return 0

    @staticmethod
    def lvm_oper():
        logger.info(" =========== LVM Operation Started =========== ")
        if Filesystem.fs_scan() == 0:
            logger.warning(
                " There are no existing filesystems found, Proceeding with further LVM configs")
            pass  # Vgcreate, Lvcreate, FScreate, mount, chown, chmod
        else:
            _, _, volumegroup_used = Filesystem.fs_scan_template()
            vgs = volumegroup_used[0].split("/")[3].split("-")[0]
            lvs = volumegroup_used[0].split("/")[3].split("-")[1]
            command1 = "pvs | grep -i %s | awk -F' ' '{print $1}'" % vgs
            pvs = check_output(command1, shell=True).split("\n")[0]
            print(vgs, lvs, pvs)
