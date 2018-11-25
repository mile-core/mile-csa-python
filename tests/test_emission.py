import unittest, time
from milecsa import Wallet
import local_config


class MyTestCase(unittest.TestCase):
    def test_something(self):

        #
        # Put your address
        #
        src = Wallet(phrase="secret-phrase")

        print(src.public_key, src.private_key)
        state = src.get_state()
        for b in state.balances:
            print(b)

        result = src.emission(asset_code=1)

        self.assertFalse(not result)

        time.sleep(41)

        state = src.get_state()
        for b in state.balances:
            print(b)


if __name__ == '__main__':
    unittest.main()
