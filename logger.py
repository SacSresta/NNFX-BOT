import logging
import os

LOG_FORMAT = "%(asctime)s %(message)s"
DEFAULT_LEVEL =logging.DEBUG

class LogWrapper():
    def __init__(self,name,mode = "a"):
        self.create_directory()
        self.filename = './logs/' + name + '.log'
        self.logger = logging.getLogger(name)
        self.logger.setLevel(DEFAULT_LEVEL)

        file_handler = logging.FileHandler(self.filename,mode=mode)
        formatter = logging.Formatter(LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.info("LogWrapper init()" + self.filename)


    def create_directory(self):
        path = './logs'
        if not os.path.exists(path):
            os.makedirs(path)
            