from milecsa import Chain, Config


#
# Print block state
#
def print_block(chain, block):
    print("Block Id:  ", block.blockId)
    print("Version:   ", block.version)
    print("Timestamp: ", block.timestamp)
    print("Trx count: ", block.transaction_count)

    #
    # Get bloc transaction
    #
    for t in block.transactions:
        asset = chain.asset_name(t.assetCode)
        print(t, t.source, "->[", t.description, "]", t.destination, " asset: ", t.assetCode, asset, " amount: ",
              t.amount)


def main():
    #
    # Set your full node url
    #
    Config.url = "https://wallet.testnet.mile.global"
    #
    # Enable client balancing
    #
    Config.useBalancing = True

    #
    # Enable debug printing
    #
    Config.rpcDebug = True

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

