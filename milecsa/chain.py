from .config import config
from .rpc import Rpc
from .transaction_parser import TransactionParser


class Block:
    def __init__(self, block_id):
        # todo lazy
        self.block_id = block_id

        self.tx_parser = TransactionParser()

        rpc = Rpc("get-block-by-id", params={"id": self.block_id})
        result = rpc.exec().result
        self.block_data = result['block-data']

        self.block_id = self.block_data['id']
        self.timestamp = self.block_data['timestamp']
        self.version = int(self.block_data['version'])
        self.transactions = []
        for tx in self.block_data['transactions']:
            self.transactions += self.tx_parser.parse(tx, self.block_id)

        # self.transaction_count = int(self.block_data['transaction-count'])
        self.transaction_count = len(self.transactions)


class Chain:

    class State:
        def __init__(self):
            rpc = Rpc("get-blockchain-state", params={})
            result = rpc.exec().result
            self.block_count = int(result['block-count'])
            self.node_count = int(result['node-count'])
            self.pending_transaction_count = int(result['pending-transaction-count'])

            # TODO !!! voing ->> voting
            self.voting_transaction_count = int(result['voing-transaction-count'])
            self.transaction_count = 0

    __response__ = None

    def __init__(self):
        if not Chain.__response__:  # todo lazy
            rpc = Rpc("get-blockchain-info", params={})
            Chain.__response__ = rpc.exec()
        self.project = Chain.__response__.result['project']
        self.version = Chain.__response__.result['version']
        self.supported_transactions = Chain.__response__.result['supported-transaction-types']
        self.supported_assets = Chain.__response__.result['supported-assets']
        self.asset_codes = {int(a['code']): a['name'] for a in self.supported_assets}
        self.asset_names = {a['name']: int(a['code']) for a in self.supported_assets}

        if config.rpcDebug:
            print("Supported assets: ", self.supported_assets)
            print("Asset codes: ", self.asset_codes)
            print("Asset names: ", self.asset_names)

    @staticmethod
    def get_current_block_id():
        rpc = Rpc("get-current-block-id", params={})
        response = rpc.exec()
        return int(response.result['current-block-id'])

    @staticmethod
    def get_block(block_id):
        return Block(block_id)

    @staticmethod
    def get_state():
        return Chain.State()

    def asset_code(self, name):
        return self.asset_names[name]

    def asset_name(self, code):
        return self.asset_codes[code]

    def __eq__(self, other):
        return (self.project == other.project) and (self.version == other.version)
