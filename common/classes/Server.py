import logging

from common.utils import get_message, send_message
from common.variables import ERROR, ACCOUNT_NAME, ACTION, EXIT, SENDER, MESSAGE_TEXT, TIME, DESTINATION, MESSAGE, \
    RESPONSE_400, RESPONSE_200, USER, PRESENCE
import select
import socket

from common.descriptors import Port, IpAddress
from common.metaclasses import ServerMaker


class Server(metaclass=ServerMaker):
    port = Port()
    addr = IpAddress()

    def __init__(self, listen_address, listen_port):
        self.addr = listen_address
        self.port = listen_port
        self.clients = []
        self.messages = []
        self.names = dict()
        self.logger = logging.getLogger('server')

    def init_socket(self):
        self.logger.info(
            f"Запущен сервер, порт для подключений: {self.port} , адрес с которого принимаются подключения: {self.addr}."
            f" Если адрес не указан, принимаются соединения с любых адресов.")
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((self.addr, self.port))
        transport.settimeout(0.5)

        self.sock = transport
        self.sock.listen()

    def main_loop(self):
        self.init_socket()

        while True:
            try:
                client, client_address = self.sock.accept()
            except OSError:
                pass
            else:
                self.logger \
                    .info(f"Установлено соедение с ПК {client_address}")
                self.clients.append(client)

            recv_data_lst = []
            send_data_lst = []
            err_lst = []
            try:
                if self.clients:
                    recv_data_lst, send_data_lst, err_lst = select.select(self.clients, self.clients, [], 0)
            except OSError:
                pass

            if recv_data_lst:
                for client_with_message in recv_data_lst:
                    try:
                        self.process_client_message(get_message(client_with_message), client_with_message)
                    except:
                        self.logger.info(f"Клиент {client_with_message.getpeername()} отключился от сервера.")
                        self.clients.remove(client_with_message)

            for message in self.messages:
                try:
                    self.process_message(message, send_data_lst)
                except:
                    self.logger.info(f"Связь с клиентом с именем {message[DESTINATION]} была потеряна")
                    self.clients.remove(self.names[message[DESTINATION]])
                    del self.names[message[DESTINATION]]
            self.messages.clear()

    def process_message(self, message, listen_socks):
        if message[DESTINATION] in self.names and self.names[message[DESTINATION]] in listen_socks:
            send_message(self.names[message[DESTINATION]], message)
            self.logger.info(
                f"Отправлено сообщение пользователю {message[DESTINATION]} от пользователя {message[SENDER]}.")
        elif message[DESTINATION] in self.names and self.names[message[DESTINATION]] not in listen_socks:
            raise ConnectionError
        else:
            self.logger.error(
                f"Пользователь {message[DESTINATION]} не зарегистрирован на сервере, отправка сообщения невозможна.")

    def process_client_message(self, message, client):
        self.logger.debug(f"Разбор сообщения от клиента : {message}")
        if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message:
            if message[USER][ACCOUNT_NAME] not in self.names.keys():
                self.names[message[USER][ACCOUNT_NAME]] = client
                send_message(client, RESPONSE_200)
            else:
                response = RESPONSE_400
                response[ERROR] = "Имя пользователя уже занято."
                send_message(client, response)
                self.clients.remove(client)
                client.close()
            return
        elif ACTION in message and message[ACTION] == MESSAGE and DESTINATION in message and TIME in message \
                and SENDER in message and MESSAGE_TEXT in message:
            self.messages.append(message)
            return
        elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message:
            self.clients.remove(self.names[ACCOUNT_NAME])
            self.names[ACCOUNT_NAME].close()
            del self.names[ACCOUNT_NAME]
            return
        else:
            response = RESPONSE_400
            response[ERROR] = "Запрос некорректен."
            send_message(client, response)
            return
