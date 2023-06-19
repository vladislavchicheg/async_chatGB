import ipaddress
import logging

logger = logging.getLogger("server")


class Port:
    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            logger.critical("В качастве порта заданно некорректное значение")
            exit(1)
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class IpAddress:
    def __set__(self, instance, value):
        try:
            ipaddress.ip_address(value)
            correct_ip = True
        except ValueError:
            correct_ip = False
        if not correct_ip and value != '':
            logger.critical(f"Попытка запуска сервера с указанием некорректного ip")
            exit(1)
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name