import unittest

from milecsa import Wallet, WebWallet

from .local_config import *


class MyTestCase(unittest.TestCase):
    def test_something(self):

        phrase = "Some secret phrase"
        pk = Wallet(phrase=phrase)
        web_wallet = WebWallet()

        l0 = web_wallet.payment_link(pk.public_key, "XDR tokens", amount=10, description="Payment descr")
        l1 = web_wallet.payment_link(pk.public_key, asset=0, amount=10, description="Payment descr")

        print()
        print(l0)
        print(l1)

        print(web_wallet.public_key_link(pk.public_key, name='Public key'))
        print(web_wallet.private_key_link(pk.private_key, name='Private key'))
        print(web_wallet.secret_phrase_link(phrase=phrase))

        q0 = web_wallet.payment_qr(pk.public_key, "XDR tokens", amount=10, description="Payment descr")
        print(q0)
        q0.save("./img-q0.png")

        q1 = web_wallet.public_key_qr(public_key=pk.public_key, name="Some public")
        print(q1)
        q1.save("./img-q1.png")

        q2 = web_wallet.private_key_qr(private_key=pk.private_key, name="Some private")
        print(q2)
        q2.save("./img-q2.png")

        q3 = web_wallet.note_qr(note="Some note")
        print(q3)
        q3.save("./img-q3.png")

        q4 = web_wallet.secret_phrase_qr(phrase=phrase)
        print(q4)
        q4.save("./img-q4.png")

        self.assertEqual(l0, l1)


if __name__ == '__main__':
    unittest.main()
