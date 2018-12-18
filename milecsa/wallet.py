from __milecsa import \
    __key_pair as key_pair, \
    __key_pair_with_secret_phrase as key_pair_with_secret_phrase, \
    __key_pair_from_private_key as key_pair_from_private_key

import milecsa
from milecsa.chain import Chain
from milecsa.rpc import Rpc
from milecsa.transaction_parser import TransactionParser
from milecsa.webwallet import WebWallet


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

        def __init__(self, balances, preferred_transaction_id):
            self.balances = balances
            self.preferred_transaction_id = preferred_transaction_id

        def get_balances(self, name=None, code=None):
            if name:
                x = [x for x in self.balances if x.asset.name == name]
            elif code:
                x = [x for x in self.balances if x.asset.code == code]
            else:
                raise ValueError("Name or value are not specified")

            return x

    def __init__(self, public_key=None, private_key=None, phrase=None, name=""):
        self.name = name
        self.phrase = phrase

        pair = {}

        if public_key and private_key:
            pair['public-key'] = public_key
            pair['private-key'] = private_key

        elif private_key:
            pair = key_pair_from_private_key(private_key)

        elif phrase:
            pair = key_pair_with_secret_phrase(phrase)

        elif public_key:
            pair['public-key'] = public_key
            pair['private-key'] = None

        else:
            pair = key_pair()

        self.public_key = pair['public-key']
        self.private_key = pair['private-key']

        self.__rpc_state = Rpc("get-wallet-state", params={"public-key": self.public_key})
        self.__chain = None
        self.__web_wallet = WebWallet()

    def __eq__(self, other):
        return (self.private_key == other.private_key) and (self.public_key == other.public_key)

    def get_chain(self):
        if not self.__chain:
            self.__chain = Chain()
        return self.__chain

    def get_state(self):  # todo cache
        response = self.__rpc_state.exec()
        balances = []
        for b in response.result['balance']:
            asset_code = int(b['code'])
            asset_name = self.get_chain().asset_name(code=asset_code)
            amount = b['amount']
            balances.append(Balance(asset=Asset(asset_name, asset_code), amount=amount))

        tx_id = int(response.result['preferred-transaction-id'])
        return Wallet.State(balances=balances,
                            preferred_transaction_id=tx_id)

    def get_transactions(self, limit=1000):
        rpc_transactions = Rpc("get-wallet-transactions", params={"public-key": self.public_key, "limit": limit})
        response = rpc_transactions.exec()

        trx_list = []
        parser = TransactionParser()
        for t in response.result['transactions']:
            trx_list += parser.parse(t['description'], -1)

        return trx_list

    def transfer(self, dest, asset_code, amount, description='', fee=0):

        if type(dest) is Wallet:
            destination = dest.public_key
        elif type(dest) is str:
            destination = dest
        else:
            raise TypeError(f"Dest must be Wallet or str, {type(dest)} passed")

        trx = milecsa.Transfer(self, asset_code, amount, destination, description, fee)
        return trx.send()

    def emission(self, asset_code, fee=0):
        tx = milecsa.Emission(self, asset_code, fee=fee)
        return tx.send()

    # web wallet #################################################################################

    def payment_qr(self, asset, amount):
        return self.__web_wallet.payment_qr(public_key=self.public_key, asset=asset, amount=amount)

    def public_key_qr(self):
        return self.__web_wallet.public_key_qr(public_key=self.public_key, name=self.name)

    def private_key_qr(self):
        return self.__web_wallet.private_key_qr(private_key=self.public_key, name=self.name)

    def phrase_qr(self):
        if not self.phrase:
            return None
        return self.__web_wallet.secret_phrase_qr(phrase=self.phrase)
