import unittest
from milecsa import Chain, Config
import local_config


def print_block(chain, block):
    print("Id:        ", block.blockId)
    print("Version:   ", block.version)
    print("Timestamp: ", block.timestamp)
    print("Trx count: ", block.transaction_count)

    for t in block.transactions:
        asset = chain.asset_name(t.assetCode)
        print(t, t.source, "->[", t.description, "]", t.destination, " asset: ", t.assetCode, asset, " amount: ",
              t.amount)


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
