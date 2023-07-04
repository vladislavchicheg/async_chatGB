"""Утилиты"""
import argparse
import ipaddress
import json
import logging
import sys
import time

from common.decorators import log
from common.variables import MAX_PACKAGE_LENGTH, ENCODING, DEFAULT_PORT, DEFAULT_IP_ADDRESS, RESPONSE, ERROR, ACTION, \
    TIME, PRESENCE, USER, ACCOUNT_NAME, LIST_INFO, REMOVE_CONTACT, USERS_REQUEST, ADD_CONTACT, GET_CONTACTS
from error import ServerError

client_logger = logging.getLogger('client')


@log
def get_message(sock):
    encoded_response = sock.recv(MAX_PACKAGE_LENGTH)
    json_response = encoded_response.decode(ENCODING)
    response = json.loads(json_response)
    if isinstance(response, dict):
        return response
    else:
        raise TypeError


@log
def send_message(sock, message):
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)


@log
def arg_parser_server(default_port, default_address):
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", default=default_port, type=int, nargs="?")
    parser.add_argument("-a", default=default_address, nargs="?")
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    return listen_address, listen_port


@log
def create_presence(account_name):
    logger = logging.getLogger('client')
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    logger.debug(
        f"Сформировано {PRESENCE} сообщение для пользователя {account_name}")
    return out


@log
def process_response_ans(message):
    logger = logging.getLogger('client')
    logger.debug(f"Разбор приветственного сообщения от сервера: {message}")
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return "200 : OK"
        elif message[RESPONSE] == 400:
            raise ValueError(f"400 : {message[ERROR]}")
    raise ValueError(RESPONSE)


@log
def arg_parser_client():
    logger = logging.getLogger('client')
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    parser.add_argument('-p', '--password', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name
    client_passwd = namespace.password

    # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        logger.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. Допустимы адреса с 1024 до 65535. Клиент завершается.')
        exit(1)

    return server_address, server_port, client_name, client_passwd

# Функция запрос контакт листа


def contacts_list_request(sock, name):
    client_logger.debug(f'Запрос контакт листа для пользователся {name}')
    req = {
        ACTION: GET_CONTACTS,
        TIME: time.time(),
        USER: name
    }
    client_logger.debug(f'Сформирован запрос {req}')
    send_message(sock, req)
    ans = get_message(sock)
    client_logger.debug(f'Получен ответ {ans}')
    if RESPONSE in ans and ans[RESPONSE] == 202:
        return ans[LIST_INFO]
    else:
        raise ServerError


# Функция добавления пользователя в контакт лист
def add_contact(sock, username, contact):
    client_logger.debug(f'Создание контакта {contact}')
    req = {
        ACTION: ADD_CONTACT,
        TIME: time.time(),
        USER: username,
        ACCOUNT_NAME: contact
    }
    send_message(sock, req)
    ans = get_message(sock)
    if RESPONSE in ans and ans[RESPONSE] == 200:
        pass
    else:
        raise ServerError('Ошибка создания контакта')
    print('Удачное создание контакта.')


# Функция запроса списка известных пользователей
def user_list_request(sock, username):
    client_logger.debug(f'Запрос списка известных пользователей {username}')
    req = {
        ACTION: USERS_REQUEST,
        TIME: time.time(),
        ACCOUNT_NAME: username
    }
    send_message(sock, req)
    ans = get_message(sock)
    if RESPONSE in ans and ans[RESPONSE] == 202:
        return ans[LIST_INFO]
    else:
        raise ServerError('Server Error')


# Функция удаления пользователя из контакт листа
def remove_contact(sock, username, contact):
    client_logger.debug(f'Создание контакта {contact}')
    req = {
        ACTION: REMOVE_CONTACT,
        TIME: time.time(),
        USER: username,
        ACCOUNT_NAME: contact
    }
    send_message(sock, req)
    ans = get_message(sock)
    if RESPONSE in ans and ans[RESPONSE] == 200:
        pass
    else:
        raise ServerError('Ошибка удаления клиента')
    print('Удачное удаление')


# Функция инициализатор базы данных. Запускается при запуске, загружает
# данные в базу с сервера.
def database_load(sock, database, username):
    # Загружаем список известных пользователей
    try:
        users_list = user_list_request(sock, username)
    except ServerError:
        client_logger.error('Ошибка запроса списка известных пользователей.')
    else:
        database.add_users(users_list)

    # Загружаем список контактов
    try:
        contacts_list = contacts_list_request(sock, username)
    except ServerError:
        client_logger.error('Ошибка запроса списка контактов.')
    else:
        for contact in contacts_list:
            database.add_contact(contact)
