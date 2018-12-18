import pprint

from milecsa import Chain, config


#
# Print block state
#
def print_block(chain, block):
    print("Block Id:  ", block.block_id)
    print("Version:   ", block.version)
    print("Timestamp: ", block.timestamp)
    print("Trx count: ", block.transaction_count)

    #
    # Get bloc transaction
    #
    pp = pprint.PrettyPrinter(indent=2)
    for t in block.transactions:
        asset = chain.asset_name(t.asset_code)
        pp.pprint([asset, t.__class__.__name__, t.__dict__])


def main():
    #
    # Set your full node url
    #
    config.web.url = "https://wallet.testnet.mile.global"
    #
    # Enable client balancing
    #
    config.useBalancing = True

    #
    # Enable debug printing
    #
    config.rpcDebug = False

    # Open chain
    chain = Chain()

    # get chain state
    state = chain.get_state()

    # last block id == state.block_count-1
    print("Block count: ", state.block_count)

    #
    # iterate last 20 blocks
    #
    print()
    for bid in range(state.block_count - 20, state.block_count):
        block = chain.get_block(block_id=bid)
        print_block(chain, block)
        print()


if __name__ == "__main__":
    main()

