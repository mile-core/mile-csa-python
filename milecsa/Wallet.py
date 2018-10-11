from __milecsa import \
    __key_pair as key_pair, \
    __key_pair_with_secret_phrase as key_pair_with_secret_phrase, \
    __key_pair_from_private_key as key_pair_from_private_key

from milecsa.Rpc import Rpc
from milecsa.Chain import Chain
from milecsa.Shared import Shared
from milecsa.TransactionParser import TransactionParser


class Asset:

    def __init__(self, name, code):
        self.name = name
        self.code = code

    def __eq__(self, other):
        return self.code == other.code and self.name == other.name

    def __str__(self):
        return '{"%s":%s}' % (self.name, self.code)


class Balance:

    def __init__(self, asset, amount):
        self.asset = asset
        self.amount = amount

    def __eq__(self, other):
        return self.asset == other.asset and self.amount == other.amount

    def __str__(self):
        return '%s: %s' % (self.asset, self.amount)


class Wallet:

    class State:

        def __init__(self, balances, last_transaction_id):
            self.balances = balances
            self.last_transaction_id = last_transaction_id

        def get_balance(self, name=None, code=None):
            if name:
                x = [x for x in self.balances if x.name == name]
            elif code:
                x = [x for x in self.balances if x.code == code]
            return x

    publicKey = None
    privateKey = None

    def __init__(self, public_key=None, private_key=None, phrase=None, name=""):

        p = {}
        self.name = name
        self.phrase = phrase

        if public_key and private_key:
            p['public-key'] = public_key
            p['private-key'] = private_key

        elif private_key:
            p = key_pair_from_private_key(private_key)

        elif phrase:
            p = key_pair_with_secret_phrase(phrase)

        elif public_key:
            p['public-key'] = public_key
            p['private-key'] = None

        else:
            p = key_pair()

        self.publicKey = p['public-key']
        self.privateKey = p['private-key']

        self.__rpc_sate = Rpc("get-wallet-state", params={"public-key": self.publicKey})
        self.__chain = Chain()
        self.__shared = Shared()

    def __eq__(self, other):
        return (self.privateKey == other.privateKey) and (self.publicKey == other.publicKey)

    def get_chain(self):
        return self.__chain

    def get_state(self):
        response = self.__rpc_sate.exec()
        balances = []
        for b in response.result['balance']:
            asset_code = int(b['code'])
            asset_name = self.__chain.asset_name(code=asset_code)
            amount = b['amount']
            balances.append(Balance(asset=Asset(asset_name, asset_code), amount=amount))

        trxid = int(response.result['last-transaction-id'])
        return Wallet.State(balances=balances,
                            last_transaction_id=trxid)

    def get_transations(self, limit=1000):
        rpc_transactions = Rpc("get-wallet-transactions", params={"public-key": self.publicKey, "limit": limit})
        response = rpc_transactions.exec()

        trx_list = []
        for t in response.result['transactions']:
            parser = TransactionParser(json_data=t['description'])
            trx_list += parser.transactions

        return trx_list

    def transfer(self, dest, asset_code, amount, description=None, fee=None):

        if type(dest) is Wallet:
            destination = dest.publicKey
        elif type(dest) is type(""):
            destination = dest

        trx = Transfer(src=self,
                       dest=destination,
                       asset_code=asset_code,
                       amount=amount,
                       description=description,
                       fee=fee)

        return trx.send()

    def emission(self, dest, asset_code, amount, description=None, fee=None):

        if type(dest) is Wallet:
            destination = dest.publicKey
        elif type(dest) is type(""):
            destination = dest

        trx = Emission(src=self,
                       dest=destination,
                       asset_code=asset_code,
                       amount=amount,
                       description=description,
                       fee=fee)

        return trx.send()

    def payment_qr(self, asset, amount):
        return self.__shared.payment_qr(public_key=self.publicKey, asset=asset, amount=amount)

    def public_key_qr(self):
        return self.__shared.public_key_qr(public_key=self.publicKey, name=self.name)

    def private_key_qr(self):
        return self.__shared.private_key_qr(private_key=self.publicKey, name=self.name)

    def phrase_qr(self):
        if not self.phrase:
            return None
        return self.__shared.secret_phrase_qr(phrase=self.phrase)
