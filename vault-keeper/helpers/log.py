#!/usr/bin/env python

import logging
from sys import stdout
from sys import exit


class SetLogging(object):
    def __init__(self):
        self.levels = ['info', 'warn', 'error']
        self.setup_logging()
        self.logger = logging.getLogger(__name__)

    def setup_logging(self):
        logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s',
                            level=logging.INFO,
                            stream=stdout)

    def set_level(self, level, message):
        for set_level in self.levels:
            if set_level == level:
                self.logger.info(message)
                break
            elif set_level == level:
                self.logger.warn(message)
                break
            elif set_level == level:
                self.logger.error(message)
                break

    def log(self, level=None, details=None, exit_code=False):
        self.set_level(level, message=details)
        if exit_code:
            exit(exit_code)


if __name__ == '__main__':
    SetLogging.setup_logging()
