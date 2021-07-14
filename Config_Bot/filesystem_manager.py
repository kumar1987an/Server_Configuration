"""
    Codename: filesystem_manager.py

    Author: Kumaran Ramalingam

    Second Parent Codename: server_config_bot.py

    First Parent Codename:  main.py
"""

# Importing required libraries
import os
import pwd
import logging
from subprocess import check_output, check_call, Popen, PIPE, call, CalledProcessError
import re
from time import sleep

# Other files importing
from file_edit import FileEdit

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


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
            command2 = (
                r"fdisk -l| grep -i sd | egrep -v '%s'| awk -F' ' '{print $2}'|awk -F':' '{print $1}'"
                % used_disks
            )
            command3 = (
                r"fdisk -l| grep -i sd | egrep -v '%s'| awk -F' ' '{print $3}'"
                % used_disks
            )
            free_pvs = check_output(command2, shell=True).split()
            free_gbs = check_output(command3, shell=True).split()
            return dict(zip(free_pvs, free_gbs))

        except CalledProcessError:
            logger.critical("No disk found empty")

    @staticmethod
    def partial_vgs_check():
        command1 = r"vgs | grep -v 'rootvg' | tail -n +2"
        command_output = check_output(command1, shell=True)
        matches = re.findall(
            r"\w+vg.|\w+.\w+$|\d\s$|\w+.\w+\s$", command_output, re.M)
        final_output = [i.strip(" ") for i in matches]
        available_free_vg_and_size = dict(
            zip(final_output[0::2], final_output[1::2]))
        return {key: value for key, value in available_free_vg_and_size.items() if value != "0"}

    @staticmethod
    def fs_backup(filesystem):  # filesystem name as input to be backed up.
        logger.info(" Filesystem {} backup Started".format(filesystem))
        dir_name = filesystem.split("/")[-1]
        Popen(
            r"tar -cvf /var/tmp/{}.tar {}".format(dir_name,
                                                  filesystem).split(),
            stdout=PIPE,
            stderr=PIPE,
        )
        tar_check = call(
            r"ls /var/tmp/{}.tar".format(dir_name).split(), stdout=PIPE, stderr=PIPE
        )

        if tar_check == 0:

            logger.info(" Filesystem {} backup completed".format(dir_name))

        else:
            logger.critical(
                " Filesystem backup not happened please login to the system and verify"
            )

    @staticmethod
    def lvm_full_scan_template():
        command1 = r"df -h | egrep -v 'root|mnt|dummy|swap|snap|udev|sd|tmpfs|boot'|tail -n +2 | awk -F' ' '{print $5}'"
        command2 = r"df -h | egrep -v 'root|mnt|dummy|swap|snap|udev|sd|tmpfs|boot'|tail -n +2 | awk -F' ' '{print $NF}'"
        command3 = r"lvs -a -o +devices | egrep -vw 'rootvg|testvg' | awk -F' ' '{print $1,$2,$NF}'|tail -n +2 | awk -F'(' '{print $1}'"
        used_percentage = check_output(command1, shell=True).decode().split()
        used_filesystem = check_output(command2, shell=True).decode().split()
        used_lv_vg_pv = check_output(command3, shell=True).decode().split("\n")
        used_lv_vg_pv.pop()  # removing last null element
        return used_percentage, used_filesystem, used_lv_vg_pv

    @staticmethod
    def check_and_wipeoutlvm(percentage_used, filesystem_used, lv_vg_pv_used):
        """This function will perform various LVM Operations like
        VG, LV, PS and FS level including backup and LVM removal"""

        logger.info(" =========== LVM Operation Started =========== ")
        for ps, fs, metadata in zip(percentage_used, filesystem_used, lv_vg_pv_used):
            lv = metadata.split()[0]
            vg = metadata.split()[1]
            pv = metadata.split()[2]

            logger.warning(
                " Proceeding with app data LVM wipeout if FS, LV, VG, PV available"
            )
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
                    logger.info(" VG {} state changed to offline".format(vg))
                    command5 = r"vgremove %s" % vg
                    Popen(command5.split(), stdout=PIPE, stderr=PIPE)
                    logger.info(
                        " VG {} has been removed from system completely".format(
                            vg)
                    )

                except Exception as e:
                    print(e)

                try:
                    command6 = r"pvremove %s" % pv
                    Popen(command6.split(), stdout=PIPE, stderr=PIPE)
                    logger.info(
                        " PV(s) {} has been removed from system completely".format(pv)
                    )

                except Exception as e:
                    print(e)

                logger.warning(" Completed with app data LVM wipeout")

            else:
                logger.critical(
                    "{} is more than 5% occupied please perform \
                                    FS backup manually and re-run the program".format(
                        fs
                    )
                )

        logger.info(" =========== LVM Operation Completed =========== ")

    @staticmethod
    def check_and_warn(lv_vg_pv_used):

        for metadata in lv_vg_pv_used:
            lv = metadata.split()[0]
            vg = metadata.split()[1]
            pv = metadata.split()[2]

            logger.critical(
                """
            These are the LVMs still in use without required filesystems
            VG: {}
            LV: {}
            PV: {}
            """.format(
                    vg, lv, pv
                )
            )

    @staticmethod
    def lvm_code_snippet(
        requested_lv_size, new_lv_name, vg_with_max_free_space, mount_name, fs_type, mount_owner, mount_group, mount_perm
    ):
        try:

            # LV create
            command1 = r"lvcreate -y -L {}G -n {}lv {}".format(
                requested_lv_size, new_lv_name, vg_with_max_free_space
            )
            check_call(command1, shell=True)
            logger.info(
                "LV {}lv has been created under volumen group {} successfully".format(
                    new_lv_name, vg_with_max_free_space
                )
            )

            sleep(3)
            # FS create
            command2 = r"mkfs.ext4 /dev/{}/{}lv -F".format(
                vg_with_max_free_space, new_lv_name
            )
            check_call(command2, shell=True)
            logger.info(
                "Filesystem {} has been formatted under LV {}".format(
                    mount_name, new_lv_name
                )
            )

        except CalledProcessError:
            logger.warning(
                "LV {}lv is already exists in LVM please check the server manually for FS not found".format(new_lv_name))

        else:

            # Mount point create
            if os.path.lexists(mount_name):
                logger.warning(
                    "Mountpoint {} already exists".format(mount_name))
            else:
                os.makedirs(mount_name)
                logger.info(
                    "Mountpoint {} has been created".format(mount_name))

            # FS entry check
            with open("/etc/fstab", "r") as fsentry:
                fsdata = fsentry.read()
                pattern = re.compile(r"{}".format(mount_name))

                if pattern.search(fsdata):
                    logger.warning(
                        "Filesystem entry already exists in /etc/fstab file")
                else:
                    # FS tab entry
                    data = r"/dev/{}/{}lv       {}    {}    defaults    0    0".format(
                        vg_with_max_free_space, new_lv_name, mount_name, fs_type
                    )
                    FileEdit.normal_append_mode("/etc/fstab", data)

            sleep(3)

            # Mount Filesystem
            command4 = r"mount -a"
            call(command4, shell=True)
            logging.info(
                "Filesystem {} has been mounted successfully".format(mount_name))

            try:
                pwd.getpwnam(mount_owner)
            except Exception as e:
                print(e)
            else:
                try:
                    os.chown(mount_name, pwd.getpwnam(
                        mount_owner).pw_uid, pwd.getpwnam(mount_owner).pw_gid)
                    logger.info(" Filesystem {} has been changed to {}:{} user group".format(
                        mount_name, mount_owner, mount_group))
                except Exception as e:
                    print(e)
                else:
                    command5 = r"chmod {} {}".format(mount_perm, mount_name)
                    check_call(command5, shell=True)
                    logger.info(" Filesystem {} has been changed to {} requested permission".format(
                        mount_name, mount_perm))
            finally:
                logger.info(
                    "================= LVM configuration Completed =================")

    @staticmethod
    def lvm_operation(
        fs_type, mount_name, mount_size, mount_owner, mount_group, mount_perm
    ):

        free_disk_and_size = Filesystem.unused_pvs_check()  # a normal dictionary
        free_disk_with_max_size = max(
            free_disk_and_size, key=free_disk_and_size.get)
        free_pv, free_pv_size = free_disk_with_max_size, free_disk_and_size.pop(
            free_disk_with_max_size
        )
        available_vg_and_free_size = (
            Filesystem.partial_vgs_check()
        )  # a normal dictionary

        vg_with_max_free_space = max(
            available_vg_and_free_size, key=available_vg_and_free_size.get
        )
        free_space_in_max_space_vg = available_vg_and_free_size.pop(
            vg_with_max_free_space
        )
        new_lv_name = mount_name.split("/")[-1]
        requested_lv_size = float(mount_size)

        # print(free_pv)
        # print(free_pv_size)
        # print(free_space_in_max_space_vg)
        # print(vg_with_max_free_space)
        # print(available_vg_and_free_size)
        # print(new_lv_name)
        # print(requested_lv_size)

        if available_vg_and_free_size:
            if free_space_in_max_space_vg[-1] == "m":
                actual_space_in_vg = float(
                    free_space_in_max_space_vg[:-1]) * 1024

            if free_space_in_max_space_vg[-1] == "g":
                actual_space_in_vg = float(free_space_in_max_space_vg[:-1])

        if available_vg_and_free_size:

            try:
                command1 = r"df -h | grep -i {}".format(mount_name)
                check_call(command1, shell=True)
                logger.warning(
                    "Filesystem {} already exists on existing vg {}".format(
                        mount_name, vg_with_max_free_space
                    )
                )
            except CalledProcessError:
                if requested_lv_size < actual_space_in_vg:
                    Filesystem.lvm_code_snippet(
                        requested_lv_size,
                        new_lv_name,
                        vg_with_max_free_space,
                        mount_name,
                        fs_type,
                        mount_owner,
                        mount_group,
                        mount_perm
                    )

        elif free_disk_and_size:
            try:
                command1 = r"df -h | grep -i {}".format(mount_name)
                check_call(command1.split(), stdout=PIPE, stderr=PIPE)
                logger.warning(
                    "Filesystem {} already exists on existing vg {}".format(
                        mount_name, vg_with_max_free_space
                    )
                )

            except CalledProcessError:
                if requested_lv_size <= free_pv_size:
                    try:
                        # PV create
                        command2 = r"pvcreate {}".format(free_pv)
                        call(command2, shell=True)
                        logger.info("PV {} has been created".format(free_pv))

                        # VG Create
                        command3 = r"vgs | egrep -v root | awk -F' ' '{print $1}'|tail -n +2"
                        child3 = check_output(command3, shell=True)
                        vgname_pattern = re.compile(r"\d", re.MULTILINE)

                        try:
                            maxvg_number = max([int(match.group())
                                                for match in vgname_pattern.finditer(child3)])
                            if maxvg_number:
                                vgname = "appvg{}".format(maxvg_number + 1)
                                command4 = r"vgcreate {} {}".format(
                                    vgname, free_pv)
                                call(command4, shell=True)
                                logger.info(
                                    "VG {} has been created on top of {}".format(
                                        vgname, free_pv
                                    )
                                )

                        except:
                            maxvg_number = 1
                            vgname = "appvg{}".format(maxvg_number)
                            command5 = r"vgcreate {} {}".format(
                                vgname, free_pv)
                            call(command5, shell=True)
                            logger.info(
                                "VG {} has been created on top of {}".format(
                                    vgname, free_pv
                                )
                            )

                        finally:
                            Filesystem.lvm_code_snippet(
                                requested_lv_size, new_lv_name, vg_with_max_free_space, mount_name, fs_type, mount_owner, mount_group, mount_perm)

                    except Exception as e:
                        print(e)
