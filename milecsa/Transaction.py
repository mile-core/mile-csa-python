from milecsa.Rpc import Rpc
from milecsa.Chain import Chain


class Transaction:

    data = None
    wallet = None
    blockid = None
    trxid = None

    def __init__(self, wallet, trxid=None):
        self.__chain = Chain()
        self.blockid = self.__chain.get_current_block_id()

        self.wallet = wallet
        if trxid:
            self.trxid = trxid
        else:
            state = self.wallet.get_state()
            self.trxid = state.last_transaction_id

    def send(self):
        self.build()
        rpc = Rpc("send-transaction", params=self.data)
        response = rpc.exec()
        return response.result

    def build(self):
        pass