# -*- coding: utf-8 -*-

"""
Output logging class
"""

import datetime
import logging
import sys

dt = datetime.datetime.now()
dt = dt.strftime("%Y%m%d")


class Logger:
    def __init__(self, log_name):
        """ """
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s',
                            handlers=[
                                logging.FileHandler(f"output{log_name}_{dt}.log")
                            ])
        self.logger = logging.getLogger()

    def Info(self, info_name):
        self.logger.info(info_name)

    def Critical(self, message):
        self.logger.critical(message, exc_info=True)

    def Warning(self, message):
        self.logger.critical(message)
