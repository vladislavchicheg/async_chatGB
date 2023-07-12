import inspect
import logging
import sys
import socket
import log.client_config
import log.server_config
import log.console_config


def log(func):
    if sys.argv[0].endswith("client.py"):
        logger = logging.getLogger("client")
    elif sys.argv[0].endswith("server.py"):
        logger = logging.getLogger("server")
    else:
        logger = logging.getLogger("console")

    def log_wraper(*args, **kwargs):
        result = func(*args, **kwargs)
        logger.info(
            f" Функция {func.__name__}() вызвана c параметрами:{args}, {kwargs} из функции "
            f"{inspect.stack()[1][3]}()", stacklevel=2)
        return result

    return log_wraper


def login_required(func):
    def checker(*args, **kwargs):
        from server.core import MessageProcessor
        from common.variables import ACTION, PRESENCE
        if isinstance(args[0], MessageProcessor):
            found = False
            for arg in args:
                if isinstance(arg, socket.socket):
                    for client in args[0].names:
                        if args[0].names[client] == arg:
                            found = True
            for arg in args:
                if isinstance(arg, dict):
                    if ACTION in arg and arg[ACTION] == PRESENCE:
                        found = True
            if not found:
                raise TypeError
        return func(*args, **kwargs)

    return checker


if __name__ == "__main__":
    @log
    def func_z():
        pass

    def main():
        func_z()

    main()
