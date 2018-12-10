from urllib.parse import quote_plus

import qrcode

from .chain import Chain
from .config import config


class WebWallet:

    def __init__(self):
        self.__chain = None

    def get_chain(self):
        if not self.__chain:
            self.__chain = Chain()
        return self.__chain

    def payment_link(self, public_key, asset, amount, description=""):
        if type(asset) == int:
            asset = self.get_chain().asset_name(code=int(asset))
        a = public_key + ":" + quote_plus(asset) + ":" + str(amount) + ":" + quote_plus(description)
        return config.web.base_url() + config.web.payment.amount + a

    @staticmethod
    def public_key_link(public_key, name=""):
        a = public_key + ":" + quote_plus(name)
        return config.web.base_url() + config.web.wallet.public_key + a

    @staticmethod
    def private_key_link(private_key, name=""):
        a = private_key + ":" + quote_plus(name)
        return config.web.base_url() + config.web.wallet.private_key + a

    @staticmethod
    def note_link(note):
        return config.web.base_url() + config.web.wallet.note + quote_plus(note)

    @staticmethod
    def secret_phrase_link(phrase):
        return config.web.base_url() + config.web.wallet.secret_phrase + quote_plus(phrase)

    def make_qr(self, data):
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
        qr.add_data(data=data)
        qr.make(fit=True)
        return qr

    def payment_qr(self, public_key, asset, amount, description=""):
        link = self.payment_link(public_key=public_key, asset=asset, amount=amount, description=description)
        image = self.make_qr(link).make_image(fill_color="black", back_color="white")
        return image

    def public_key_qr(self, public_key, name=""):
        link = self.public_key_link(public_key=public_key, name=name)
        image = self.make_qr(link).make_image(fill_color="black", back_color="white")
        return image

    def private_key_qr(self, private_key, name=""):
        link = self.private_key_link(private_key=private_key, name=name)
        image = self.make_qr(link).make_image(fill_color="black", back_color="white")
        return image

    def note_qr(self, note):
        link = self.note_link(note=note)
        image = self.make_qr(link).make_image(fill_color="black", back_color="white")
        return image

    def secret_phrase_qr(self, phrase):
        link = self.secret_phrase_link(phrase=phrase)
        image = self.make_qr(link).make_image(fill_color="black", back_color="white")
        return image
