from data_extraction import DataExtract
from argparse import ArgumentParser
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


def main():
    """Argument parser"""
    parser = ArgumentParser()
    help_doc = """Adhoc requests are fs, ng, ug, sw, cr, pk and all -->
                  fs = filesystems, ng = netgroups,
                  ug = users_groups, sw = softwares,
                  cr = cronusers, pk = pubkeys,
                  all = all categories
               """
    parser.add_argument("--adhoc", type=str, required=True, help=help_doc, nargs="+")
    parser.add_argument(
        "--user",
        type=str,
        required=True,
        help="Enter the username for location to save the jsons",
    )

    args = parser.parse_args()
    DataExtract.load_file(args)


if __name__ == "__main__":
    main()
