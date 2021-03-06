import unittest
from milecsa import Rpc
from .local_config import *


class MyTestCase(unittest.TestCase):
    def test_something(self):

        req0 = Rpc("get-blockchain-info", params={})
        req1 = Rpc("get-blockchain-info", params={})

        for i in range(0, 10):
            print(req0.get_url())

        response0 = req0.exec()
        response1 = req1.exec()

        print(response0.result, response0.id)

        self.assertFalse(response0.id < response1.id)


if __name__ == '__main__':
    unittest.main()
