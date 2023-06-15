import logging
import threading
import time

from common.metaclasses import ClientMaker
from common.utils import send_message
from common.variables import ACTION, EXIT, TIME, ACCOUNT_NAME, MESSAGE, SENDER, DESTINATION, MESSAGE_TEXT


class ClientSender(threading.Thread, metaclass=ClientMaker):
    def __init__(self, account_name, sock):
        self.account_name = account_name
        self.sock = sock
        self.logger = logging.getLogger('client')
        super().__init__()

    def create_exit_message(self):
        return {
            ACTION: EXIT,
            TIME: time.time(),
            ACCOUNT_NAME: self.account_name
        }

    def create_message(self):
        to = input("Введите получателя сообщения: ")
        message = input("Введите сообщение для отправки: ")
        message_dict = {
            ACTION: MESSAGE,
            SENDER: self.account_name,
            DESTINATION: to,
            TIME: time.time(),
            MESSAGE_TEXT: message
        }
        self.logger.debug(f"Сформирован словарь сообщения: {message_dict}")
        try:
            send_message(self.sock, message_dict)
            self.logger.info(f"Отправлено сообщение для пользователя {to}")
        except:
            self.logger.critical("Потеряно соединение с сервером.")
            exit(1)

    def run(self):
        self.print_help()
        while True:
            command = input("Введите команду: ")
            if command == "message":
                self.create_message()
            elif command == "help":
                self.print_help()
            elif command == "exit":
                try:
                    send_message(self.sock, self.create_exit_message())
                except:
                    pass
                print("Завершение соединения.")
                self.logger.info("Завершение работы по команде пользователя.")
                time.sleep(1)
                break
            else:
                print("Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.")

    def print_help(self):
        print("Поддерживаемые команды:")
        print("message - отправить сообщение. Кому и текст будет запрошены отдельно.")
        print("help - вывести подсказки по командам")
        print("exit - выход из программы")
