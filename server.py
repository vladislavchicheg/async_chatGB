import sys
import json
from socket import *
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, ALERT, LOGIN
from common.utils import get_message, send_message


def process_client_message(message):
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][LOGIN] == 'Guest':
        return {RESPONSE: 200,
                ALERT: "OK"}
    return {
        RESPONSE: 400,
        ERROR: "Bad Request"
    }


def main():
    if "-p" in sys.argv:
        listen_port = int(sys.argv[sys.argv.index("-p") + 1])
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError("Неверный номер порта!")
    else:
        listen_port = DEFAULT_PORT
    if "-a" in sys.argv:
        listen_address = sys.argv[sys.argv.index("-a") + 1]
    else:
        listen_address = ""

    s = socket(AF_INET, SOCK_STREAM)
    s.bind((listen_address, listen_port))
    s.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = s.accept()
        try:
            message_from_cient = get_message(client)
            print(message_from_cient)
            # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
            response = process_client_message(message_from_cient)
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Принято некорретное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    main()
