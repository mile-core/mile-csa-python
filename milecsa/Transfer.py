from __milecsa import __transfer_assets as transfer_assets
from .Wallet import Wallet
from .Transaction import Transaction
import json


class BaseTransfer(Transaction):

    def __init__(self, src, dest, asset_code, amount, description=None, fee=None, trxid=None):

        Transaction.__init__(self, wallet=src, trxid=trxid)

        self.assetCode = int(asset_code)
        self.amount = str(amount)

        if type(dest) is Wallet:
            self.destination = dest.publicKey
        else:
            self.destination = dest

        if type(src) is Wallet:
            self.source = src.publicKey
        else:
            self.source = src

        self.description = description
        self.fee = fee


class Transfer(BaseTransfer):

    def build(self):
        __data = transfer_assets(self.wallet.publicKey,
                                 self.wallet.privateKey,
                                 self.destination,
                                 self.blockid,
                                 self.trxid,
                                 self.assetCode,
                                 self.amount,
                                 self.description,
                                 self.fee)
        self.data = json.loads(__data)
