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

            # Loading main Excel File
            file_in = pd.ExcelFile(
                os.path.join("/kmrnr8501/server_config", "config_input.xlsx")
            )

            # Extractor Loading
            if args.adhoc in ["FS", "fs"]:
                output = file_in.parse("filesystems")
                with open(os.path.join(path, "filesystems.json"), "w") as f:
                    f.writelines(output.to_json(orient="records"))
                logger.info(f" filesystems.json Created: Success")

            elif args.adhoc in ["NG", "ng"]:
                output = file_in.parse("netgroups")
                with open(os.path.join(path, "netgroups.json"), "w") as f:
                    f.writelines(output.to_json(orient="records"))
                logger.info(f" netgroups.json Created: Success")

            elif args.adhoc in ["PK", "pk"]:
                output = file_in.parse("pubkeys")
                with open(os.path.join(path, "pubkeys.json"), "w") as f:
                    f.writelines(output.to_json(orient="records"))
                logger.info(f" pubkeys.json Created: Success")

            elif args.adhoc in ["UG", "ug"]:
                output = file_in.parse("users_groups")
                with open(os.path.join(path, "users_groups.json"), "w") as f:
                    f.writelines(output.to_json(orient="records"))
                logger.info(f" users_groups.json Created: Success")

            elif args.adhoc in ["SW", "sw"]:
                output = file_in.parse("softwares")
                with open(os.path.join(path, "softwares.json"), "w") as f:
                    f.writelines(output.to_json(orient="records"))
                logger.info(f" softwares.json Created: Success")

            elif args.adhoc in ["CR", "cr"]:
                output = file_in.parse("cronusers")
                with open(os.path.join(path, "cronusers.json"), "w") as f:
                    f.writelines(output.to_json(orient="records"))
                logger.info(f" cronusers.json Created: Success")

            elif args.adhoc in ["ALL", "all"]:
                for i in file_in.sheet_names:
                    output = file_in.parse(i)
                    with open(os.path.join(path, i + ".json"), "w") as f:
                        f.writelines(output.to_json(orient="records"))
                    logger.info(f" {i}.json Created: Success")
            else:
                logger.warning(f" '{args.adhoc}' is not a valid adhoc request\n")
                logger.warning(
                    f" Please check the 'python main.py -h' command before execution"
                )

        else:
            logger.critical(
                " Filesystem not mounted for copying the json, please re-mount the NFS share and execute the script"
            )
