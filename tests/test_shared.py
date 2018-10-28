import unittest
from milecsa.Shared import Shared
from milecsa.Wallet import Wallet
from milecsa import Config
import local_config


class MyTestCase(unittest.TestCase):
    def test_something(self):


        phrase = "Some secret phrase"
        pk = Wallet(phrase=phrase)
        shared = Shared()

        l0 = shared.payment_link(public_key=pk.publicKey, asset="XDR tokens", amount=10)
        l1 = shared.payment_link(public_key=pk.publicKey, asset=0, amount=10)

        print()
        print(l0)
        print(l1)

        print(shared.public_key_link(public_key=pk.publicKey))
        print(shared.secret_phrase_link(phrase=phrase))

        q0 = shared.payment_qr(public_key=pk.publicKey, asset="XDR", amount=10)
        print(q0)
        q0.save("./img-q0.png")

        q1 = shared.public_key_qr(public_key=pk.publicKey, name="Some")
        print(q1)
        q1.save("./img-q1.png")

        q2 = shared.private_key_qr(private_key=pk.privateKey, name="Some private")
        print(q2)
        q2.save("./img-q2.png")

        q3 = shared.note_qr(note="Some note")
        print(q3)
        q3.save("./img-q3.png")

        q4 = shared.secret_phrase_qr(phrase=phrase)
        print(q4)
        q4.save("./img-q4.png")

        self.assertEqual(l0, l1)


if __name__ == '__main__':
    unittest.main()
