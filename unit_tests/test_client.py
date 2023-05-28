import unittest

from client import create_presence, process_response
from common.variables import TIME, ACTION, PRESENCE, USER, LOGIN, RESPONSE, ERROR


class ClientTestCase(unittest.TestCase):

    def test_def_presence(self):
        test = create_presence()
        test[TIME] = 1.1
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1.1, USER: {LOGIN: 'Guest'}})

    def test_200_response(self):
        self.assertEqual(process_response({RESPONSE: 200}), '200 : OK')

    def test_400_response(self):
        self.assertEqual(process_response({RESPONSE: 400, ERROR: 'Bad Request'}), '400 : Bad Request')

    def test_no_response(self):
        self.assertRaises(ValueError, process_response, {ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
