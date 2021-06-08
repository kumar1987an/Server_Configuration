# Importing Libraries
import os
from shutil import rmtree
import logging
from subprocess import PIPE, Popen, call
import pandas as pd


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


class DataExtract:

    # Loading main Excel File
    file_in = pd.ExcelFile(
        os.path.join("/kmrnr8501/server_config", "config_input.xlsx")
    )

    @staticmethod
    def extractor_function(user, config_type, json_filename):
        output = DataExtract.file_in.parse(config_type)
        with open(os.path.join(f"/dummyfs/{user}", json_filename), "w") as f:
            f.writelines(output.to_json(orient="records"))
            logger.info(f" {json_filename} Created: Success")

    @staticmethod
    def load_file(args):
        """Excel Data Extractor"""

        ps1 = Popen("df -h".split(), stdout=PIPE)
        ps2 = call("grep -i dummy".split(), stdin=ps1.stdout, stdout=PIPE)

        if ps2 == 0:  # Main condition check for NFS share exists
            path = f"/dummyfs/{args.user}"

            if os.path.exists(path):
                rmtree(path)
                logger.info(f" Re-creating fresh copy of Directory '{args.user}'")
                os.makedirs(path)
                logger.info(f" Directory '{args.user}' Created: Success")

            else:
                logger.warning(
                    f" Directory '{args.user}' not found creating it for you, sit tight..."
                )
                logger.info(f" Directory '{args.user}' Created: Success")
                os.makedirs(path)

            # Extractor Loading
            for adhoc in args.adhoc:
                if adhoc == "fs":
                    DataExtract.extractor_function(
                        args.user, "filesystems", "filesystems.json"
                    )
                if adhoc == "ng":
                    DataExtract.extractor_function(
                        args.user, "netgroups", "netgroups.json"
                    )
                if adhoc == "pk":
                    DataExtract.extractor_function(args.user, "pubkeys", "pubkeys.json")
                if adhoc == "ug":
                    DataExtract.extractor_function(
                        args.user, "users_groups", "usergroups.json"
                    )
                if adhoc == "sw":
                    DataExtract.extractor_function(
                        args.user, "softwares", "softwares.json"
                    )
                if adhoc == "cr":
                    DataExtract.extractor_function(
                        args.user, "cronusers", "cronusers.json"
                    )
                if adhoc == "all":
                    DataExtract.extractor_function(
                        args.user, "filesystems", "filesystems.json"
                    )
                    DataExtract.extractor_function(
                        args.user, "netgroups", "netgroups.json"
                    )
                    DataExtract.extractor_function(args.user, "pubkeys", "pubkeys.json")
                    DataExtract.extractor_function(
                        args.user, "users_groups", "usergroups.json"
                    )
                    DataExtract.extractor_function(
                        args.user, "softwares", "softwares.json"
                    )
                    DataExtract.extractor_function(
                        args.user, "cronusers", "cronusers.json"
                    )

        else:
            logger.critical(
                " Filesystem not mounted for copying the json, please re-mount the NFS share and execute the script"
            )
