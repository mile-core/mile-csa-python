from __milecsa import __emission as emission
from .Transfer import BaseTransfer
import json


class Emission(BaseTransfer):

    def build(self):
        __data = emission(self.wallet.publicKey,
                          self.wallet.privateKey,
                          self.destination,
                          self.blockid,
                          self.trxid,
                          self.assetCode,
                          self.amount,
                          self.description,
                          self.fee)
        self.data = json.loads(__data)
