"""
    Codename: filesystem_manager.py

    Author: Kumaran Ramalingam

    Second Parent Codename: server_config_bot.py

    First Parent Codename:  main.py
"""

# Importing required libraries
import os
import logging
from subprocess import check_output, Popen, PIPE, call, CalledProcessError
import re
from collections import OrderedDict
# Other files importing

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


# noinspection SpellCheckingInspection
class Filesystem(object):

    @staticmethod
    def disk_scan():
        logger.debug(" Proceeding system wide disk scan")
        ps1 = Popen("ls /sys/class/scsi_host/".split(), stdout=PIPE)
        for i in ps1.communicate()[0].decode().split():
            try:
                os.system(
                    "echo '- - -' > /sys/class/scsi_host/{}/scan".format(i))
                logger.debug(" System wide Disk Scan Completed successfully")

            except Exception as e:
                print(e)

    @staticmethod
    def unused_pvs_check():
        command1 = r"pvs | awk -F' ' '{print $1}' | tail -n +2"
        used_pvs = check_output(command1, shell=True)
        pattern = re.compile(r"sd[a-z]")
        matches = [i.group(0) for i in pattern.finditer(used_pvs)]
        used_disks = ""
        for index in range(len(matches)):
            if index == len(matches) - 1:
                used_disks = used_disks + matches[index] + "|sda"
            else:
                used_disks = used_disks + matches[index] + "|"
        try:
            command2 = r"fdisk -l| grep -i sd | egrep -v '%s'| awk -F' ' '{print $2}'|awk -F':' '{print $1}'" % used_disks
            command3 = r"fdisk -l| grep -i sd | egrep -v '%s'| awk -F' ' '{print $3}'" % used_disks
            free_pvs = check_output(command2, shell=True).split()
            free_gbs = check_output(command3, shell=True).split()
            return dict(zip(free_pvs, free_gbs))

        except CalledProcessError:
            print("No disks found empty")

    @staticmethod
    def partial_vgs_check():
        command1 = r"vgs | egrep -v  'root|app' | tail -n +2 | awk -F' ' '{print $1}'"
        command2 = r"vgs | egrep -v  'root|app' | tail -n +2 | awk -F' ' '{print $NF}'"
        recently_used_vgs = check_output(command1, shell=True).split()
        freespace_on_recently_used_vgs = check_output(command2, shell=True).split()
        tuple_for_size_and_unit = [(float(size[:-1]), size[-1].upper()) for size in freespace_on_recently_used_vgs]
        return dict(zip(recently_used_vgs, tuple_for_size_and_unit))

    @staticmethod
    def fs_backup(filesystem):  # filesystem name as input to be backed up.
        logger.info(" Filesystem {} backup Started".format(filesystem))
        dir_name = filesystem.split("/")[3]
        Popen(r"tar -cvf /var/tmp/{}.tar {}".format(dir_name,
                                                    filesystem).split(), stdout=PIPE, stderr=PIPE)
        tar_check = call(
            r"ls /var/tmp/{}.tar".format(dir_name).split(), stdout=PIPE, stderr=PIPE)

        if tar_check == 0:

            logger.info(" Filesystem {} backup completed".format(dir_name))

        else:
            logger.critical(
                " Filesystem backup not happened please login to the system and verify")

    @staticmethod
    def lvm_full_scan_template():
        command1 = r"df -h | egrep -v 'root|mnt|dummy|swap|snap|udev|sd|tmpfs|boot'|tail -n +2 | awk -F' ' '{print $5}'"
        command2 = r"df -h | egrep -v 'root|mnt|dummy|swap|snap|udev|sd|tmpfs|boot'|tail -n +2 | awk -F' ' '{print $NF}'"
        command3 = r"lvs -a -o +devices | egrep -v 'root|app' | awk -F' ' '{print $1,$2,$NF}'|tail -n +2 | awk -F'(' '{print $1}'"
        used_percentage = check_output(command1, shell=True).decode().split()
        used_filesystem = check_output(command2, shell=True).decode().split()
        used_lv_vg_pv = check_output(command3, shell=True).decode().split("\n")
        used_lv_vg_pv.pop()  # removing last null element
        return used_percentage, used_filesystem, used_lv_vg_pv

    @staticmethod
    def check_and_wipeoutlvm(percentage_used, filesystem_used, lv_vg_pv_used):
        """ This function will perform various LVM Operations like
        VG, LV, PS and FS level including backup and LVM removal """

        logger.info(" =========== LVM Operation Started =========== ")
        for ps, fs, metadata in zip(percentage_used, filesystem_used, lv_vg_pv_used):
            lv = metadata.split()[0]
            vg = metadata.split()[1]
            pv = metadata.split()[2]

            logger.warning(
                " Proceeding with app data LVM wipeout if FS, LV, VG, PV available")
            if ps in ["1%", "2%", "3%", "4%", "5%"]:

                Filesystem().fs_backup(fs)  # Backup function call

                try:
                    command2 = r"umount %s" % fs
                    Popen(command2.split(), stdout=PIPE, stderr=PIPE)
                    logger.info(
                        " FS {} has been un-mounted successfully".format(fs))

                except Exception as e:
                    print(e)

                try:
                    command3 = r"lvremove -f /dev/%s/%s" % (vg, lv)
                    Popen(command3.split(), stdout=PIPE, stderr=PIPE)
                    logger.info(
                        " LV {} has been remove successfully".format(lv))

                except Exception as e:
                    print(e)

                try:
                    command4 = r"vgchange -an %s" % vg
                    Popen(command4.split(), stdout=PIPE, stderr=PIPE)
                    logger.info(
                        " VG {} state changed to offline".format(vg))
                    command5 = r"vgremove %s" % vg
                    Popen(command5.split(), stdout=PIPE, stderr=PIPE)
                    logger.info(
                        " VG {} has been removed from system completely".format(vg))

                except Exception as e:
                    print(e)

                try:
                    command6 = r"pvremove %s" % pv
                    Popen(command6.split(), stdout=PIPE, stderr=PIPE)
                    logger.info(
                        " PV(s) {} has been removed from system completely".format(pv))

                except Exception as e:
                    print(e)

                logger.warning(" Completed with app data LVM wipeout")

            else:
                logger.critical("{} is more than 5% occupied please perform \
                                    FS backup manually and re-run the program".format(fs))

        logger.info(" =========== LVM Operation Completed =========== ")

    @staticmethod
    def check_and_warn(lv_vg_pv_used):

        for metadata in lv_vg_pv_used:
            lv = metadata.split()[0]
            vg = metadata.split()[1]
            pv = metadata.split()[2]

            logger.critical("""
            These are the LVMs still in use without required filesystems 
            VG: {}
            LV: {}
            PV: {}
            """.format(vg, lv, pv))

    @staticmethod
    def lvm_operation(fs_type, mount_name, mount_size, mount_owner, mount_group, mount_perm):
        # ======================= Working LVM create ==========================
        # variables: fs_type, mount_name, mount_size, mount_grp, mount_owner, mount_perm
        unused_pvs_and_size = OrderedDict(sorted(Filesystem.unused_pvs_check().items()))  # a dictionary
        partial_vgs_data = Filesystem.partial_vgs_check()  # a dictionary
        unit_pattern_finder = re.search(r"[a-zA-Z]", mount_size.upper()).group()
        given_mount_size_string = mount_size.partition(unit_pattern_finder)
        # =====================================================================
