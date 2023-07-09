import unittest

from common.variables import ACTION, PRESENCE, TIME, USER, LOGIN, RESPONSE, ERROR, ALERT
from server_old import process_client_message


class ServerTestCase(unittest.TestCase):
    err_dict = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }
    ok_dict = {
        RESPONSE: 200,
        ALERT: 'OK'
    }

    def test_no_action(self):
        self.assertEqual(process_client_message(
            {TIME: '1.1', USER: {LOGIN: 'Guest'}}), self.err_dict)

    def test_wrong_action(self):
        self.assertEqual(process_client_message(
            {ACTION: 'CREATE', TIME: '1.1', USER: {LOGIN: 'Guest'}}), self.err_dict)

    def test_no_time(self):
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, USER: {LOGIN: 'Guest'}}), self.err_dict)

    def test_no_user(self):
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: '1.1'}), self.err_dict)

    def test_bad_user(self):
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: 1.1, USER: {LOGIN: 'Vasya'}}), self.err_dict)

    def test_ok_check(self):
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: 1.1, USER: {LOGIN: 'Guest'}}), self.ok_dict)


if __name__ == '__main__':
    unittest.main()
