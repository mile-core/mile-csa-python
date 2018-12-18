from .transactions import RegisterNode, UnregisterNode, PostTokenRate


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

    def post_token_rate(self, rate, fee=0):
        tx = PostTokenRate(self.wallet, rate, fee)
        return tx.send()
