"""
    Codename: file_edit.py

    Author: Kumaran Ramalingam

    Second Parent Codename: server_config_bot.py

    First Parent Codename:  do_main.py
"""

import logging
import re
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


class FileEdit(object):
    """this class is to edit file_name (Dynamic)"""

    @staticmethod
    def append_mode(file_name, data):
        """Function definition: for appending data to a file_name"""

        if os.path.basename(file_name) == "passwd":
            with open(file_name, "a") as a_file:
                a_file.writelines("+@{}:x:::::\n".format(data))
            logger.info(" '%s' --> appended to the file_name %s" % (data, file_name))

        elif os.path.basename(file_name) == "group":
            with open(file_name, "a") as a_file:
                a_file.writelines("+:::\n")
            logger.info(" '%s' --> appended to the file_name %s" % (data, file_name))

        elif os.path.basename(file_name) == "cron.allow":
            with open(file_name, "a") as a_file:
                a_file.writelines("{}\n".format(data))
            logger.info(" '%s' --> appended to the file_name %s" % (data, file_name))

        elif os.path.basename(file_name) == "shadow":
            with open(file_name, "a") as a_file:
                a_file.writelines("{}\n".format(data))
            logger.info(" Shadow data has been appended to the file_name")
        else:
            with open(file_name, "a") as a_file:
                a_file.writelines("{}\n".format(data))
            logger.info(("Given data has been appended to the file name {}".format(file_name)))

    @staticmethod
    def find_replace(file_name, search_pattern, replace_pattern):
        """Function definition: for find and replace data to a file_name"""

        for s_pattern, r_pattern in zip(search_pattern, replace_pattern):

            if os.path.basename(file_name) == "nsswitch.conf":

                with open(file_name, "r") as in_file:
                    content = in_file.read()

                if s_pattern == "passwd:.+":
                    output_content = re.sub(s_pattern, r_pattern, content)

                elif s_pattern == "group:.+":
                    output_content = re.sub(s_pattern, r_pattern, content)

                elif s_pattern == "shadow:.+":
                    output_content = re.sub(
                        s_pattern, r_pattern, content, count=1)

                else:
                    output_content = re.sub(s_pattern, r_pattern, content)
                try:
                    with open(file_name, "w") as out_file:
                        out_file.write(output_content)
                    logger.info(
                        " Given {} are matched and replaced over the temp file_name {}".format(
                            s_pattern, file_name)
                    )

                except Exception as e:
                    logger.critical(e)

            else:
                pass  # Need to add codes if further files to be edited based on situation

    @staticmethod
    def find_remove():
        pass

    @staticmethod
    def append_lineaware_mode(file_name, data, position="up"):
        """ Appending data exactly above """

        if file_name == "/etc/shadow":
            FileEdit.append_mode(file_name, data)

        else:

            with open(file_name, "r") as read_file:
                content = read_file.readlines()

            line_number = ""

            for i, j in enumerate(content):

                if re.findall(r"\B\+", j):
                    if position == "up":
                        line_number = line_number + str(i)
                        break
                    elif position == "down":
                        line_number = line_number + str(i+1)
                        break

            # appending the content one line above of given search pattern
            content.insert(int(line_number),
                           "{}\n".format(data))

            if file_name == "/etc/passwd":
                dir_name = data.split(":")[5]
                try:
                    with open(file_name, "w") as write_file:
                        write_file.writelines(content)
                    logger.info(
                        " User data has been appened to {}".format(file_name))
                    logger.warning(
                        " Tyring to create Home directory {}".format(dir_name))
                    os.makedirs(dir_name)
                    logger.info(
                        "{} Home directory created successfully".format(dir_name))

                except Exception as e:
                    logger.warning(e)

            elif file_name == "/etc/group":
                try:
                    with open(file_name, "w") as write_file:
                        write_file.writelines(content)
                    logger.info(
                        " Group data has been appended to {}".format(file_name))

                except Exception as e:
                    logger.warning(e)
