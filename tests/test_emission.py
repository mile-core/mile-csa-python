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

        result = src.emission(asset_code=1)

        self.assertFalse(not result)

        time.sleep(21)

        state = src.get_state()
        for b in state.balances:
            print(b)


if __name__ == '__main__':
    unittest.main()
