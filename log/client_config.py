import sys
import os
import logging
from common.variables import LOGGING_LEVEL, ENCODING, CLIENT_LOG_FILE, LOG_FORMATTER

sys.path.append('../')

CLIENT_FORMATTER = logging.Formatter(LOG_FORMATTER)

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, CLIENT_LOG_FILE)
STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(CLIENT_FORMATTER)
STREAM_HANDLER.setLevel(logging.ERROR)
LOG_FILE = logging.FileHandler(PATH, encoding=ENCODING)
LOG_FILE.setFormatter(CLIENT_FORMATTER)

LOGGER = logging.getLogger('client')
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(LOG_FILE)
LOGGER.setLevel(LOGGING_LEVEL)

# отладка
if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Отладочная информация')
    LOGGER.info('Информационное сообщение')
