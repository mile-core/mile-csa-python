from __milecsa import __transfer_assets as transfer_assets
from .Wallet import Wallet
from .Transaction import Transaction


class BaseTransfer(Transaction):

    def __init__(self, src, asset_code, amount=0.0, dest=None, description=None, fee=0.0, trxid=None):

        Transaction.__init__(self, wallet=src, trxid=trxid)

        self.assetCode = int(asset_code)

        if amount:
            self.amount = float(amount)
        else:
            self.amount = None

        if type(dest) is Wallet:
            self.destination = dest.publicKey
        else:
            self.destination = dest

        if type(src) is Wallet:
            self.source = src.publicKey
        else:
            self.source = src

        if description is None:
            self.description = ""
        else:
            self.description = description

        if fee:
            self.fee = float(fee)
        else:
            self.fee = float(0)


class Transfer(BaseTransfer):

    def build(self):
        self.data = transfer_assets(self.wallet.publicKey,
                                    self.wallet.privateKey,
                                    self.destination,
                                    self.blockid,
                                    self.trxid,
                                    self.assetCode,
                                    self.amount,
                                    self.fee,
                                    self.description)
