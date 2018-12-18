import unittest
from time import sleep

from milecsa import Node, Wallet
from .local_config import *


class MyTestCase(unittest.TestCase):
    def test_something(self):
        #
        # Put your address
        #
        w = Wallet(phrase="secret-phrase")
        print(w.public_key, w.private_key)
        state = w.get_state()
        for b in state.balances:
            print(b)

        # result = w.emission(asset_code=1)

        node = Node(w, '1.2.3.4')

        result = node.register(10001)
        self.assertFalse(not result)

        sleep(42)

        result = node.post_token_rate(1.41)
        self.assertFalse(not result)

        sleep(42)

        result = node.unregister()
        self.assertFalse(not result)


if __name__ == '__main__':
    unittest.main()
