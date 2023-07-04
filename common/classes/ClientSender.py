import logging
import threading
import time

from common.metaclasses import ClientMaker
from common.utils import send_message, add_contact
from common.variables import ACTION, EXIT, TIME, ACCOUNT_NAME, MESSAGE, SENDER, DESTINATION, MESSAGE_TEXT
from error import ServerError

logger = logging.getLogger('client')
sock_lock = threading.Lock()
database_lock = threading.Lock()


class ClientSender(threading.Thread, metaclass=ClientMaker):
    def __init__(self, account_name, sock, database):
        self.account_name = account_name
        self.sock = sock
        self.logger = logging.getLogger('client')
        self.database = database
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
        except BaseException:
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
                except BaseException:
                    pass
                print("Завершение соединения.")
                self.logger.info("Завершение работы по команде пользователя.")
                time.sleep(1)
                break
            else:
                print(
                    "Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.")

    def print_help(self):
        print('Поддерживаемые команды:')
        print('message - отправить сообщение. Кому и текст будет запрошены отдельно.')
        print('history - история сообщений')
        print('contacts - список контактов')
        print('edit - редактирование списка контактов')
        print('help - вывести подсказки по командам')
        print('exit - выход из программы')

    def print_history(self):
        ask = input(
            'Показать входящие сообщения - in, исходящие - out, все - просто Enter: ')
        with database_lock:
            if ask == 'in':
                history_list = self.database.get_history(
                    to_who=self.account_name)
                for message in history_list:
                    print(
                        f'\nСообщение от пользователя: {message[0]} от {message[3]}:\n{message[2]}')
            elif ask == 'out':
                history_list = self.database.get_history(
                    from_who=self.account_name)
                for message in history_list:
                    print(
                        f'\nСообщение пользователю: {message[1]} от {message[3]}:\n{message[2]}')
            else:
                history_list = self.database.get_history()
                for message in history_list:
                    print(
                        f'\nСообщение от пользователя: {message[0]}, пользователю {message[1]} от {message[3]}\n{message[2]}')

    # Функция изменеия контактов
    def edit_contacts(self):
        ans = input('Для удаления введите del, для добавления add: ')
        if ans == 'del':
            edit = input('Введите имя удаляемного контакта: ')
            with database_lock:
                if self.database.check_contact(edit):
                    self.database.del_contact(edit)
                else:
                    logger.error('Попытка удаления несуществующего контакта.')
        elif ans == 'add':
            # Проверка на возможность такого контакта
            edit = input('Введите имя создаваемого контакта: ')
            if self.database.check_user(edit):
                with database_lock:
                    self.database.add_contact(edit)
                with sock_lock:
                    try:
                        add_contact(self.sock, self.account_name, edit)
                    except ServerError:
                        logger.error(
                            'Не удалось отправить информацию на сервер.')
