import unittest, time
from milecsa.Wallet import Wallet
from milecsa.Config import Config
from .local_config import *


class MyTestCase(unittest.TestCase):
    def test_something(self):


        #
        # Put your address
        #
        src = Wallet(phrase="secret-phrase")

        print(src.publicKey, src.privateKey)

        #
        # Put your address
        #
        dst = Wallet(phrase="destination-secret-phrase")

        result = src.transfer(dest=dst, asset_code=0, amount=0.1, description="back my money!")

        self.assertFalse(not result)

        time.sleep(21)

        state = dst.get_state()
        for b in state.balances:
            print(b)


if __name__ == '__main__':
    unittest.main()
