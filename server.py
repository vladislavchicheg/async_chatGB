import logging
import select
import sys
import time
from socket import *

import log.server_config
from common.variables import ACTION, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, LOGIN, MESSAGE, MESSAGE_TEXT, SENDER
from common.utils import get_message, send_message
import logging
import select
import sys
import time
from socket import *

import log.server_config
from common.utils import get_message, send_message
from common.variables import ACTION, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, LOGIN, MESSAGE, MESSAGE_TEXT, SENDER

CLIENT_LOGGER = logging.getLogger('server')


def process_client_message(message, messages_list, client):
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][LOGIN] == 'Guest':
        send_message(client, {RESPONSE: 200})
        return
    if ACTION in message and message[ACTION] == MESSAGE and \
            TIME in message and MESSAGE_TEXT in message:
        messages_list.append((message[LOGIN], message[MESSAGE_TEXT]))
        return
    send_message(client, {
        RESPONSE: 400,
        ERROR: "Bad Request"
    })
    return


def parse_args():
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        CLIENT_LOGGER.critical("После параметра -\'p\' не указан номер порта.")
        sys.exit(1)
    except ValueError:
        CLIENT_LOGGER.critical("В качастве порта заданно некорректное значение")
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = int(sys.argv[sys.argv.index('-a') + 1])
        else:
            listen_address = ''
    except IndexError:
        CLIENT_LOGGER.critical("После параметра -\'a\' не указан IP адрес.")
        sys.exit(1)

    return listen_address, listen_port


def main():
    listen_address, listen_port = parse_args()
    CLIENT_LOGGER.info(f'Запущен сервер - порт: {listen_port} ; адрес:{listen_address}')
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((listen_address, listen_port))
    s.settimeout(1)
    s.listen(MAX_CONNECTIONS)
    clients = []
    messages = []

    while True:
        try:
            client, client_address = s.accept()
        except OSError:
            pass
        else:
            CLIENT_LOGGER.info(f"Установлено соедение - {client_address}")
            clients.append(client)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []
        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    process_client_message(get_message(client_with_message),
                                           messages, client_with_message)
                except:
                    CLIENT_LOGGER.info(f"Клиент {client_with_message.getpeername()} "
                                       f"отключился от сервера.")
                    clients.remove(client_with_message)

        if messages and send_data_lst:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_lst:
                try:
                    send_message(waiting_client, message)
                except:
                    CLIENT_LOGGER.info(f"Клиент {waiting_client.getpeername()} отключился от сервера.")
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()
