import logging
from common.classes.Server import Server
from common.utils import arg_parser_server

logger = logging.getLogger('server')


def main():
    listen_address, listen_port = arg_parser_server()
    server = Server(listen_address, listen_port)
    server.main_loop()


if __name__ == '__main__':
    main()
