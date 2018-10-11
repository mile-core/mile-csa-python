import unittest
from milecsa.Wallet import Wallet
from milecsa.Config import Config


class MyTestCase(unittest.TestCase):
    def test_something(self):

        Config.sslVerification = False
        Config.connectionTimeout = 30
        Config.url = "http://node002.testnet.mile.global"
        Config.useBalancing = False
        Config.rpcDebug = True

        wallet0 = Wallet(phrase="Some secrete phrase")

        print()
        print(wallet0.publicKey, wallet0.privateKey)

        #
        # Put your address
        #
        wallet1 = Wallet(public_key="...")

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
        wallet2 = Wallet(public_key="...")
        trx = wallet2.get_transations()
        for t in trx:
            asset = wallet2.get_chain().asset_name(t.assetCode)
            print(t, t.source, "->[", t.description, "]", t.destination, " asset: ", t.assetCode, asset, " amount: ", t.amount)


if __name__ == '__main__':
    unittest.main()
