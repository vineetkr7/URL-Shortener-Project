import logging
import logging.handlers
from common import logger_name, logger_level


class Logger:
    def __init__(self, name, level):
        self.logger = logging.getLogger(name)
        self.logger_level = level

    def set_level(self):
        logging_level = None
        if self.logger_level in 'DEBUG':
            logging_level = logging.DEBUG
        if self.logger_level in 'INFO':
            logging_level = logging.INFO
        if self.logger_level in 'CRITICAL':
            logging_level = logging.CRITICAL
        if self.logger_level in 'WARNING':
            logging_level = logging.WARNING
        if self.logger_level in 'ERROR':
            logging_level = logging.ERROR

        return logging_level

    def create_logger(self):
        formatter = logging.Formatter('%(asctime)s - %(name)s - '
                                      '%(levelname)s - %(message)s')
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler('logs.log')
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        self.logger.setLevel(self.set_level())
        return self.logger


logger = Logger(logger_name, logger_level)
