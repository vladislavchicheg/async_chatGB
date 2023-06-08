import argparse
import json
import logging
import sys
import time
import log.client_config
from socket import *
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, LOGIN, MESSAGE, MESSAGE_TEXT, SENDER
from common.utils import get_message, send_message

CLIENT_LOGGER = logging.getLogger('client')
def create_presence(login='Guest'):
    message = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            LOGIN: login
        }
    }
    return message


def process_response(data):
    CLIENT_LOGGER.debug(f'получено сообщение от сервера: {data}')
    if RESPONSE in data:
        if data[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {data[ERROR]}'
    raise ValueError



def message_from_server(message):
    if ACTION in message and message[ACTION] == MESSAGE and \
            SENDER in message and MESSAGE_TEXT in message:
        print(f"Получено сообщение от пользователя "
              f"{message[SENDER]}:\n{message[MESSAGE_TEXT]}")
        CLIENT_LOGGER.info(f"Получено сообщение от пользователя "
                           f"{message[SENDER]}:\n{message[MESSAGE_TEXT]}")
    else:
        CLIENT_LOGGER.error(f"Получено некорректное сообщение с сервера: {message}")



def create_message(sock, login='Guest'):
    message = input("Введите сообщение для отправки или \'!!!\' для завершения работы: ")
    if message == "!!!":
        sock.close()
        CLIENT_LOGGER.info("Завершение работы по команде пользователя.")
        print("Спасибо за использование нашего сервиса!")
        sys.exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        LOGIN: login,
        MESSAGE_TEXT: message
    }
    CLIENT_LOGGER.debug(f"Сформирован словарь сообщения: {message_dict}")
    return message_dict



def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("addr", default=DEFAULT_IP_ADDRESS, nargs="?")
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs="?")
    parser.add_argument("-m", "--mode", default="listen", nargs="?")
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical(f"Попытка запуска клиента с неподходящим номером порта: {server_port}.")
        sys.exit(1)

    if client_mode not in ("listen", "send"):
        CLIENT_LOGGER.critical(f"Указан недопустимый режим работы {client_mode}, "
                               f"допустимые режимы: listen , send")
        sys.exit(1)

    return server_address, server_port, client_mode


def main():
    server_address, server_port, client_mode = arg_parser()
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((server_address, server_port))
    message_to_server = create_presence()
    send_message(s, message_to_server)
    try:
        answer = process_response(get_message(s))
        CLIENT_LOGGER.info(f'получен ответ сервера: {answer}')
        print(answer)
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать сообщение сервера.')
        print('Не удалось декодировать сообщение сервера.')
        sys.exit(1)
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}')
        sys.exit(1)
    else:

        # основной цикл прогрммы:
        if client_mode == "send":
            print("Режим работы - отправка сообщений.")
        if client_mode == "listen":
            print("Режим работы - приём сообщений.")
        while True:
            # режим работы - отправка сообщений
            if client_mode == "send":
                try:
                    send_message(s, create_message(s))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f"Соединение с сервером {server_address} было потеряно.")
                    sys.exit(1)

            # Режим работы приём:
            if client_mode == "listen":
                try:
                    message_from_server(get_message(s))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f"Соединение с сервером {server_address} было потеряно.")
                    sys.exit(1)


if __name__ == "__main__":
    main()
