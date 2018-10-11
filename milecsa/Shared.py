from urllib.parse import quote_plus
from milecsa.Chain import Chain
from milecsa.Config import Config
import qrcode


class Shared:

    def __init__(self):
        self.__chain = Chain()

    def payment_link(self, public_key, asset, amount, name=""):
        if type(asset) == int:
            asset = self.__chain.asset_name(code=int(asset))
        a = public_key + ":" + asset + ":" + str(amount) + ":" + quote_plus(name)
        return Config.baseUrl() + Config.Shared.Payment.amount + a

    @staticmethod
    def public_key_link(public_key, name=""):
        a = public_key + ":" + quote_plus(name)
        return Config.baseUrl() + Config.Shared.Wallet.publicKey + a

    @staticmethod
    def private_key_link(private_key, name=""):
        a = private_key + ":" +  quote_plus(name)
        return Config.baseUrl() + Config.Shared.Wallet.privateKey + a

    @staticmethod
    def note_link(note):
        return Config.baseUrl() + Config.Shared.Wallet.note + quote_plus(note)

    @staticmethod
    def secret_phrase_link(phrase):
        return Config.baseUrl() + Config.Shared.Wallet.secretPhrase + quote_plus(phrase)

    def make_qr(self, data):
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
        qr.add_data(data=data)
        qr.make(fit=True)
        return qr

    def payment_qr(self, public_key, asset, amount, name=""):
        image = self.make_qr(data=self.payment_link(public_key=public_key, asset=asset, amount=amount, name=name))\
            .make_image(fill_color="black", back_color="white")
        return image

    def public_key_qr(self, public_key, name=""):
        image = self.make_qr(data=self.public_key_link(public_key=public_key, name=name))\
            .make_image(fill_color="black", back_color="white")
        return image

    def private_key_qr(self, private_key, name=""):
        image = self.make_qr(data=self.private_key_link(private_key=private_key, name=name))\
            .make_image(fill_color="black", back_color="white")
        return image

    def note_qr(self, note):
        image = self.make_qr(data=self.note_link(note=note))\
            .make_image(fill_color="black", back_color="white")
        return image

    def secret_phrase_qr(self, phrase):
        image = self.make_qr(data=self.secret_phrase_link(phrase=phrase))\
            .make_image(fill_color="black", back_color="white")
        return image
