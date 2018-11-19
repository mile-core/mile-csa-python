import unittest
from milecsa.Wallet import Wallet
from milecsa.Config import Config
from .local_config import *


class MyTestCase(unittest.TestCase):

    def test_something(self):

        wallet0 = Wallet(phrase="secret-phrase")

        print()
        print(wallet0.publicKey, wallet0.privateKey)

        #
        # Put your address
        #
        wallet1 = Wallet(phrase="destination-secret-phrase")

        state = wallet0.get_state()
        print()
        print(state.balances, state.last_transaction_id, wallet0.publicKey)
        for b in state.balances:
            print(b)

        wqr0 = wallet0.phrase_qr()
        print(wqr0)
        wqr0.save("./img-wqr0.png")

        wqr1 = wallet0.payment_qr(asset=1, amount=10)
        print(wqr1)
        wqr1.save("./img-wqr1.png")

        #
        # Put your address
        #
        wallet2 = Wallet(phrase="destination-secret-phrase")
        trx = wallet2.get_transations()
        for t in trx:
            asset = wallet2.get_chain().asset_name(t.assetCode)
            print(t, t.source, "->[", t.description, "]", t.destination, " asset: ", t.assetCode, asset, " amount: ", t.amount)


if __name__ == '__main__':
    unittest.main()
