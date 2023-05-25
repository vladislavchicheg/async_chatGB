import sys
import json
from socket import *


def process_client_message(message):
    if message.get("action") == "presence" and "time" in message and "user" in message:
        return {"response": 200,
                "alert": "OK"}
    return {
        "response": 400,
        "error": "Bad Request"
    }


def main():
    if "-p" in sys.argv:
        listen_port = int(sys.argv[sys.argv.index("-p") + 1])
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError("Неверный номер порта!")
    else:
        listen_port = 7777
    if "-a" in sys.argv:
        listen_address = sys.argv[sys.argv.index("-a") + 1]
    else:
        listen_address = ""

    s = socket(AF_INET, SOCK_STREAM)
    s.bind((listen_address, listen_port))
    s.listen(5)

    while True:
        client, client_address = s.accept()
        try:
            encoded_response = client.recv(1024)
            if isinstance(encoded_response, bytes):
                json_response = encoded_response.decode("utf-8")
                response = json.loads(json_response)
                if isinstance(response, dict):
                    message_from_client = response
                else:
                    raise ValueError
            else:
                raise ValueError

            response = process_client_message(message_from_client)
            json_message = json.dumps(response)
            encoded_message = json_message.encode("utf-8")
            client.send(encoded_message)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Принято некорретное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    main()
