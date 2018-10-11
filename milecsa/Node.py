from __milecsa import __register_node as register_node, __unregister_node as unregister_node
from milecsa import Wallet, Transaction


class Node(Transaction):

    address = None

    def __init__(self, wallet, address, assetCode, amount):

        Transaction.__init__(self, wallet=wallet)

        self.assetCode = int(assetCode)
        self.amount = str(amount)

        self.address = address

    def register(self):
        return register_node(self.wallet.publicKey,
                             self.wallet.privateKey,
                             self.address,
                             self.blockid,
                             self.trxid,
                             self.assetCode,
                             self.amount)

    def unregister(self):
        return unregister_node(self.wallet.publicKey,
                               self.wallet.privateKey,
                               self.blockid,
                               self.trxid)
