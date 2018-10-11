import unittest, time
from milecsa.Wallet import Wallet
from milecsa.Config import Config


class MyTestCase(unittest.TestCase):
    def test_something(self):

        Config.sslVerification = False
        Config.connectionTimeout = 30

        Config.url = "http://node002.testnet.mile.global"
        Config.useBalancing = False
        Config.rpcDebug = True

        #
        # Put your address
        #
        src = Wallet(private_key="...")

        print(src.publicKey, src.privateKey)

        #
        # Put your address
        #
        dst = Wallet(public_key="...")

        result = src.emission(dest=dst, asset_code=1, amount=1)

        self.assertFalse(not result)

        time.sleep(60)

        state = dst.get_state()
        for b in state.balances:
            print(b)


if __name__ == '__main__':
    unittest.main()
