import argparse
import json
import sys
import time
from socket import *
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT, LOGIN
from common.utils import get_message, send_message


def create_presence(login='Guest'):
    message = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            LOGIN: login
        }
    }
    return message


def precess_response(data):
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
        raise ValueError("Указан неверный порт")

    s = socket(AF_INET, SOCK_STREAM)
    s.connect((server_address, server_port))
    message_to_server = create_presence()
    send_message(s, message_to_server)
    try:
        answer = precess_response(get_message(s))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера.')


if __name__ == "__main__":
    main()
