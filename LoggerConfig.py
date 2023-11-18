import logging
from colorlog import ColoredFormatter
class CustomColoredFormatter(ColoredFormatter):
    LEVEL_NAMES = {
        logging.DEBUG: '[DEBUG]',
        logging.INFO: '[INFO]',
        logging.WARNING: '[WARNING]',
        logging.ERROR: '[ERROR]',
        logging.CRITICAL: '[CRITICAL]'
    }

    def format(self, record):
        record.levelname = self.LEVEL_NAMES.get(record.levelno, record.levelname)
        return super().format(record)

formatter = CustomColoredFormatter(
    "%(log_color)s%(levelname)s %(message)s (%(asctime)s)",
    datefmt='%Y-%m-%d %H:%M:%S',
    log_colors={
        '[DEBUG]': 'cyan',
        '[INFO]': 'yellow',
        '[WARNING]': 'orange',
        '[ERROR]': 'red',
        '[CRITICAL]': 'red,bg_white',
    }
)


stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger = logging.getLogger('my_global_logger')
logger.setLevel(logging.DEBUG)  # Set the minimum log level
logger.addHandler(stream_handler)  # Add the handler to the logger
logger.propagate = False


