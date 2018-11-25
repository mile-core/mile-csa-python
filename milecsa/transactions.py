from __milecsa import __transfer_assets as transfer_assets, __emission as emission

from milecsa.chain import Chain
from milecsa.rpc import Rpc

from .wallet import Wallet


class Transaction:

    def __init__(self, wallet, tx_id=None):
        self.data = None
        self.wallet = wallet

        self.__chain = Chain()  # todo lazy
        self.block_id = self.__chain.get_current_block_id()  # todo lazy

        if tx_id:
            self.tx_id = tx_id
        else:
            state = self.wallet.get_state()
            self.tx_id = state.preferred_transaction_id  # todo lazy

    def send(self):
        self.build()
        rpc = Rpc("send-transaction", params=self.data)
        response = rpc.exec()
        return response.result

    def build(self):
        pass


class TransactionWithFee(Transaction):

    def __init__(self, wallet, fee=0.0, tx_id=None):
        super().__init__(wallet, tx_id)
        self.fee = float(fee)


class BaseTransfer(TransactionWithFee):

    def __init__(self, src, asset_code, amount=0.0, dest=None, description=None, fee=0.0, tx_id=None):

        super().__init__(src, fee, tx_id)

        self.asset_code = int(asset_code)

        if amount:
            self.amount = float(amount)  # todo decimal/str?
        else:
            self.amount = None

        if type(dest) is Wallet:
            self.destination = dest.public_key
        else:
            self.destination = dest

        if type(src) is Wallet:
            self.source = src.public_key
        else:
            self.source = src

        self.description = description


class Transfer(BaseTransfer):

    def build(self):
        self.data = transfer_assets(self.wallet.public_key,
                                    self.wallet.private_key,
                                    self.destination,
                                    self.block_id,
                                    self.tx_id,
                                    self.asset_code,
                                    self.amount,
                                    self.fee,
                                    self.description)


class Emission(TransactionWithFee):

    def __init__(self, wallet, asset_code, fee=0.0, tx_id=None):
        super().__init__(wallet, fee, tx_id)
        self.asset_code = int(asset_code)

    def build(self):
        self.data = emission(self.wallet.public_key,
                             self.wallet.private_key,
                             self.block_id,
                             self.tx_id,
                             self.asset_code,
                             self.fee)
