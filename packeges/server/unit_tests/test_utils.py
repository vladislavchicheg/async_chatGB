"""Unit-тесты утилит"""

from common.utils import get_message, send_message
from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE, ENCODING
import sys
import os
import unittest
import json

sys.path.append(os.path.join(os.getcwd(), '..'))


class TestSocket:
    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.recv_message = None

    def send(self, message_to_send):
        json_test_message = json.dumps(self.test_dict)
        self.encoded_message = json_test_message.encode(ENCODING)
        self.recv_message = message_to_send

    def recv(self, max_len):
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)


class UtilsTestCase(unittest.TestCase):
    test_dict_send = {
        ACTION: PRESENCE,
        TIME: 111111.111111,
        USER: {
            ACCOUNT_NAME: 'Guest'
        }
    }
    test_dict_response_ok = {RESPONSE: 200}
    test_dict_response_err = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    def test_send_message(self):
        test_socket = TestSocket(self.test_dict_send)
        send_message(test_socket, self.test_dict_send)
        self.assertEqual(test_socket.encoded_message, test_socket.recv_message)
        with self.assertRaises(Exception):
            send_message(test_socket, test_socket)

    def test_get_message(self):
        test_socket_ok = TestSocket(self.test_dict_response_ok)
        test_socket_err = TestSocket(self.test_dict_response_err)
        self.assertEqual(
            get_message(test_socket_ok),
            self.test_dict_response_ok)
        self.assertEqual(
            get_message(test_socket_err),
            self.test_dict_response_err)


if __name__ == '__main__':
    unittest.main()
