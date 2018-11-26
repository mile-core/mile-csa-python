from __milecsa import __register_node as register_node, __unregister_node as unregister_node
from milecsa import Wallet, Transaction


class RegisterNode(Transaction):

    def __init__(self, wallet, address, amount, fee=0, trxid=None):
        super().__init__(wallet, trxid)
        self.fee = fee
        self.amount = amount
        self.address = address

    def build(self):
        self.data = register_node(self.wallet.publicKey,
                                  self.wallet.privateKey,
                                  self.address,
                                  self.blockid,
                                  self.trxid,
                                  self.amount,
                                  self.fee)


class UnregisterNode(Transaction):

    def __init__(self, wallet, fee=0, trxid=None):
        super().__init__(wallet, trxid)
        self.fee = fee

    def build(self):
        self.data = unregister_node(self.wallet.publicKey,
                                    self.wallet.privateKey,
                                    self.blockid,
                                    self.trxid,
                                    self.fee)


class Node:
    def __init__(self, wallet, address):
        self.address = address
        self.wallet = wallet

    def register(self, amount, fee=0):
        tx = RegisterNode(self.wallet, self.address, amount, fee)
        return tx.send()

    def unregister(self, fee=0):
        tx = UnregisterNode(self.wallet, fee)
        return tx.send()
