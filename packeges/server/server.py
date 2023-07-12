import configparser
import logging
import os
import sys
import threading

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QMessageBox

from server.database import ServerStorage

from common.utils import arg_parser_server
from server.main_window import MainWindow
from server.core import MessageProcessor

logger = logging.getLogger('server')
new_connection = False
conflag_lock = threading.Lock()


def main():
    config = configparser.ConfigParser()

    dir_path = os.getcwd()
    config.read(f"{dir_path}/{'server.ini'}")
    listen_address, listen_port = arg_parser_server(config['SETTINGS']['Default_port'],
                                                    config['SETTINGS']['Listen_Address'])
    database = ServerStorage(
        os.path.join(
            config['SETTINGS']['Database_path'],
            config['SETTINGS']['Database_file']))
    server = MessageProcessor(listen_address, listen_port, database)
    server.daemon = True
    server.start()

    # Создаём графическое окуружение для сервера:
    server_app = QApplication(sys.argv)
    server_app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
    main_window = MainWindow(database, server, config)
    server_app.exec_()
    server.running = False




if __name__ == '__main__':
    main()
