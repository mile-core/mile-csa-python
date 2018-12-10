import time
import unittest

from milecsa import Wallet

from .local_config import *

class MyTestCase(unittest.TestCase):
    def test_something(self):

        #
        # Put your address
        #
        src = Wallet(phrase="secret-phrase")
        print(src.public_key)
        for b in src.get_state().balances:
            print(b)

        #
        # Put your address
        #
        dst = Wallet(phrase="destination-secret-phrase")
        print(dst.public_key)
        for b in dst.get_state().balances:
            print(b)
        result = src.transfer(dest=dst, asset_code=0, amount=0.01, description="transfer test")

        self.assertFalse(not result)

        time.sleep(41)

        for b in dst.get_state().balances:
            print(b)


if __name__ == '__main__':
    unittest.main()
