import pprint
import unittest
from milecsa import Chain
from .local_config import *


def print_block(chain, block):
    print()
    print("Id:        ", block.block_id)
    print("Version:   ", block.version)
    print("Timestamp: ", block.timestamp)
    print("Trx count: ", block.transaction_count)

    pp = pprint.PrettyPrinter(indent=2)
    for t in block.transactions:
        asset = chain.asset_name(t.asset_code)
        pp.pprint([asset, t.__class__.__name__, t.__dict__])


class MyTestCase(unittest.TestCase):
    def test_something(self):

        chain = Chain()

        state = chain.get_state()

        print("Block count: ", state.block_count)
        print("Node count:  ", state.node_count)

        block_id = chain.get_current_block_id()
        print("Last block id: ", chain.get_current_block_id())

        block = chain.get_block(block_id=556)

        print("Last id:   ", block_id)
        print_block(chain, block)

        #
        # iterate
        #
        print()
        for bid in range(state.block_count-10, state.block_count):
            block = chain.get_block(block_id=bid)
            print_block(chain, block)
            print()

        #self.assertEqual(chain0, chain1)


if __name__ == '__main__':
    unittest.main()
