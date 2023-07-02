import json
import logging
import time
import socket

from common.classes.ClientReader import ClientReader
from common.classes.ClientSender import ClientSender
from common.classes.ORM.ClientStorage import ClientDatabase
from common.utils import send_message, get_message, arg_parser_client, create_presence, process_response_ans, \
    database_load

logger = logging.getLogger('client')


def main():
    print("Консольный месседжер. Клиентский модуль.")

    server_address, server_port, client_name = arg_parser_client()

    if not client_name:
        client_name = input("Введите имя пользователя: ")
    else:
        print(f"Клиентский модуль запущен с именем: {client_name}")

    logger.info(
        f"Запущен клиент с парамертами: адрес сервера: {server_address}, "
        f"порт: {server_port}, имя пользователя: {client_name}")

    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.settimeout(1)
        transport.connect((server_address, server_port))
        send_message(transport, create_presence(client_name))
        answer = process_response_ans(get_message(transport))
        logger.info(f"Установлено соединение с сервером. Ответ сервера: {answer}")
        print(f"Установлено соединение с сервером.")
    except json.JSONDecodeError:
        logger.error("Не удалось декодировать полученную Json строку.")
        exit(1)
    except:
        logger.error(f"Возникла ошибка")
        exit(1)
    else:
        # Инициализация БД
        database = ClientDatabase(client_name)
        database_load(transport, database, client_name)

        # Если соединение с сервером установлено корректно, запускаем поток взаимодействия с пользователем
        module_sender = ClientSender(client_name, transport, database)
        module_sender.daemon = True
        module_sender.start()
        logger.debug('Запущены процессы')

        # затем запускаем поток - приёмник сообщений.
        module_receiver = ClientReader(client_name, transport, database)
        module_receiver.daemon = True
        module_receiver.start()

        while True:
            time.sleep(1)
            if module_receiver.is_alive() and module_sender.is_alive():
                continue
            break


if __name__ == '__main__':
    main()
