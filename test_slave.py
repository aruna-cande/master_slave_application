import unittest
from slave import Slave
from unittest.mock import patch


class TestSlave(unittest.TestCase):

    def setUp(self):
        self.slave = Slave(1)

    @patch('slave.requests.get')
    def test_postmanEchoRequest_success(self, mock_get):
        mock_get.return_value.status_code = 200
        self.slave.delay = 1
        result = self.slave.postmanEchoRequest()

        self.assertTrue(mock_get.called)
        self.assertEqual(result, 0)

    @patch('slave.requests.get')
    def test_postmanEchoRequest_(self, mock_get):
        mock_get.return_value.status_code = 400
        self.slave.delay = 1
        result = self.slave.postmanEchoRequest()

        self.assertTrue(mock_get.called)
        self.assertEqual(result, 1)


if __name__ == '__main__':
    unittest.main()
