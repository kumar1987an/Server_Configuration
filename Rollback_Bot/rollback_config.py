"""
    Codename: rollback_config.py

    Author: Kumaran Ramalingam

    Parent Codename:  rollback_me.py
"""

# Importing Libraries
import json
import logging
import os

# Other files importing

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s:%(asctime)s:%(name)s:%(message)s")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


class RollBackBot:
    @staticmethod
    def execute():
        pass
