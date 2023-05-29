import logging
import sys
import json
from socket import *
import log.server_config
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, ALERT, LOGIN
from common.utils import get_message, send_message

CLIENT_LOGGER = logging.getLogger('server')
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
            CLIENT_LOGGER.critical(f'Попытка запуска сервера с недопустимым портом: {listen_port}')
            raise ValueError("Неверный номер порта!")
    else:
        listen_port = DEFAULT_PORT
    if "-a" in sys.argv:
        listen_address = sys.argv[sys.argv.index("-a") + 1]
    else:
        listen_address = ""
    CLIENT_LOGGER.info(f'Запущен сервер - порт: {listen_port} ; адрес:{listen_address}')
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((listen_address, listen_port))
    s.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = s.accept()
        try:
            message_from_cient = get_message(client)
            CLIENT_LOGGER.info(f'Получено сообщение от клиента: {message_from_cient}')
            print(message_from_cient)
            response = process_client_message(message_from_cient)
            CLIENT_LOGGER.debug(f'Отправлено сообщение клиенту: {response}')
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            CLIENT_LOGGER.error(f'Принято некорретное сообщение от клиента:{message_from_cient}')
            print('Принято некорретное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    main()
