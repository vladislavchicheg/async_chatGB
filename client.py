import argparse
import json
import logging
import sys
import time
import log.client_config
from socket import *
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, LOGIN
from common.utils import get_message, send_message
from common.decorators import log

CLIENT_LOGGER = logging.getLogger('client')


@log
def create_presence(login='Guest'):
    message = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            LOGIN: login
        }
    }
    return message


@log
def process_response(data):
    CLIENT_LOGGER.debug(f'получено сообщение от сервера: {data}')
    if RESPONSE in data:
        if data[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {data[ERROR]}'
    raise ValueError


def main():
    if sys.argv[1]:
        server_address = sys.argv[1]
    else:
        server_address = DEFAULT_IP_ADDRESS
    if sys.argv[2]:
        server_port = int(sys.argv[2])
    else:
        server_port = DEFAULT_PORT

    if server_port < 1024 or server_port > 65535:
        CLIENT_LOGGER.critical(f'Попытка запуска клиента с недопустимым портом: {server_port}')
        raise ValueError("Указан неверный порт")
    CLIENT_LOGGER.info(f'запущен клиент с адресом: {server_address}; порт: {server_port}')

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
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}')


if __name__ == "__main__":
    main()
