import logging
import threading

from common.metaclasses import ClientMaker
from common.utils import get_message
from common.variables import ACTION, MESSAGE, MESSAGE_TEXT, SENDER, DESTINATION


class ClientReader(threading.Thread, metaclass=ClientMaker):
    def __init__(self, account_name, sock):
        self.account_name = account_name
        self.sock = sock
        self.logger = logging.getLogger('client')
        super().__init__()

    def run(self):
        while True:
            try:
                message = get_message(self.sock)
                if ACTION in message and message[ACTION] == MESSAGE and SENDER in message and DESTINATION in message \
                        and MESSAGE_TEXT in message and message[DESTINATION] == self.account_name:
                    print(f"\nПолучено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}")
                    self.logger.info(f"Получено сообщение от пользователя {message[SENDER]}:\n{message[MESSAGE_TEXT]}")
                else:
                    self.logger.error(f"Получено некорректное сообщение с сервера: {message}")
            except:
                self.logger.critical("Потеряно соединение с сервером.")
                break