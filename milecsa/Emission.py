from __milecsa import __emission as emission
from .Transfer import BaseTransfer


class Emission(BaseTransfer):

    def build(self):
        self.data = emission(self.wallet.publicKey,
                             self.wallet.privateKey,
                             self.blockid,
                             self.trxid,
                             self.assetCode,
                             self.fee)
