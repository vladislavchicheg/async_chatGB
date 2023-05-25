import argparse
import json
import sys
import time
from socket import *


def create_presence(login='Vasya'):
    message = {
        "action": "presence",
        "time": time.time(),
        "user": {
            "login": login
        }
    }
    return message


def precess_response(data):
    if "response" in data:
        if data['response'] == 200:
            return '200 : OK'
        return f'400 : {data["error"]}'
    raise ValueError


def main():
    if sys.argv[1]:
        server_address = sys.argv[1]
    else:
        server_address = "127.0.0.1"
    if sys.argv[2]:
        server_port = int(sys.argv[2])
    else:
        server_port = 7777

    if server_port < 1024 or server_port > 65535:
        raise ValueError("Указан неверный порт")

    s = socket(AF_INET, SOCK_STREAM)
    s.connect((server_address, server_port))
    message_to_server = create_presence()
    json_message = json.dumps(message_to_server)
    encoded_message = json_message.encode("utf-8")
    s.send(encoded_message)
    try:
        encoded_response = s.recv(1024)
        if isinstance(encoded_response, bytes):
            json_response = encoded_response.decode("utf-8")
            response = json.loads(json_response)
            if isinstance(response, dict):
                answer = precess_response(response)
                print(answer)
            else:
                raise ValueError
        else:
            raise ValueError
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера.')


if __name__ == "__main__":
    main()
