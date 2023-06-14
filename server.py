import logging
import select
import sys
import time
from socket import *

import log.server_config
from common.variables import ACTION, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, LOGIN, MESSAGE, MESSAGE_TEXT, SENDER, DESTINATION, EXIT
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


def process_client_message(message, messages_list, client, clients, names):
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message:
        if message[USER][LOGIN] not in names.keys():
            names[message[USER][LOGIN]] = client
            send_message(client, {RESPONSE: 200})
        else:
            send_message(client, {
                RESPONSE: 400,
                ERROR: 'Имя пользователя уже занято.'
            })
            clients.remove(client)
            client.close()
        return
    elif ACTION in message and message[ACTION] == MESSAGE and \
            DESTINATION in message and TIME in message \
            and SENDER in message and MESSAGE_TEXT in message:
        messages_list.append(message)
        return
    elif ACTION in message and message[ACTION] == EXIT and LOGIN in message:
        clients.remove(names[message[LOGIN]])
        names[message[LOGIN]].close()
        del names[message[LOGIN]]
        return
    send_message(client, {
        RESPONSE: 400,
        ERROR: "Bad Request"
    })
    return


def process_message(message, names, listen_socks):

    if message[DESTINATION] in names and names[message[DESTINATION]] in listen_socks:
        send_message(names[message[DESTINATION]], message)
        CLIENT_LOGGER.info(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                    f'от пользователя {message[SENDER]}.')
    elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_socks:
        raise ConnectionError
    else:
        CLIENT_LOGGER.error(
            f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, '
            f'отправка сообщения невозможна.')
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
    names = dict()
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
                                           messages, client_with_message, clients, names)
                except:
                    CLIENT_LOGGER.info(f"Клиент {client_with_message.getpeername()} "
                                       f"отключился от сервера.")
                    clients.remove(client_with_message)
        CLIENT_LOGGER.critical(messages)
        for i in messages:
            try:
                process_message(i, names, send_data_lst)
            except Exception:
                CLIENT_LOGGER.info(f'Связь с клиентом с именем {i[DESTINATION]} была потеряна')
                clients.remove(names[i[DESTINATION]])
                del names[i[DESTINATION]]
        messages.clear()


if __name__ == '__main__':
    main()
