import unittest
from master import Master
from unittest.mock import MagicMock
from parameterized import parameterized
import asyncio


class TestSlave(unittest.TestCase):

    def setUp(self):
        self.master = Master()

    # Mock async calls
    def __AsyncMock(self, *args, **kwargs):
        m = unittest.mock.MagicMock(*args, **kwargs)

        async def mock_coro(*args, **kwargs):
            return m(*args, **kwargs)

        mock_coro.mock = m
        return mock_coro

    @parameterized.expand([
        (0,),
        (1,),
    ])
    def test_RequestFromSlave(self, mock_result):
        self.master.executeComandAsync = self.__AsyncMock(
            return_value=mock_result)

        self.master.requestFromSlave()

        if mock_result == 0:
            for slave in self.master.slave_dict:
                self.assertEqual(
                    self.master.slave_dict[slave].exit_code, mock_result)


if __name__ == '__main__':
    unittest.main()
