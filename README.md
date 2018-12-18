# Requirements 

1. Python3
1. setuptools
1. git
1. gcc >= 7.0
1. boost >= 1.66.0
1. openssl (libssl-dev)


# Tested on:

1. Centos 7 (gcc 7.x)
1. Ubuntu 17.04
1. OSX 10.13

# Build & Install

## Global

    $ git clone https://github.com/mile-core/mile-csa-python
    $ cd mile-csa-python
    $ git submodule update --init --recursive --remote
    $ python3 ./setup.py build
    $ sudo python3 ./setup.py install

## In virtual environment via pipenv

    $ pipenv install -e git+https://github.com/mile-core/mile-csa-python@master#egg=milecsa

Also you can use specific version: just replace master with target version
    
# Boost updates (if it needs)

    $ wget https://dl.bintray.com/boostorg/release/1.66.0/source/boost_1_66_0.tar.gz
    $ tar -xzf boost_1_*
    $ cd boost_1_*
    $ ./bootstrap.sh --prefix=/usr
    $ ./b2 install --prefix=/usr --with=all -j4
        
    
# Test

    $ python3 -m unittest
     
     
# Examples

### Global configuration
```python
from milecsa import config

#
# disable SSL verification
#
# config.sslVerification = False

#
# set up user defined connection timeout
#
config.connectionTimeout = 30 # seconds

#
# use MILE testnet 
#
config.web.url = "https://wallet.testnet.mile.global"

```

### Wallet create

[github](https://github.com/mile-core/mile-csa-python/tree/master/examples/wallet_create.py)

```python
from milecsa import Wallet


def main():

    wallet0 = Wallet(phrase="Some phrase")

    print(wallet0.public_key, wallet0.private_key)

    #
    # Put your address
    #
    wallet1 = Wallet(public_key="...")

    state = wallet1.get_state()
    print(state.balances, state.preferred_transaction_id, wallet1.public_key)
    for b in state.balances:
        print(b)

    #
    # Keep Secret phrase to qrcode
    #
    wqr0 = wallet0.phrase_qr()
    print(wqr0)
    wqr0.save("./img-wqr0.png")

    #
    # Generate Payment Ticket
    #
    wqr1 = wallet0.payment_qr(asset=1, amount=10)
    print(wqr1)
    wqr1.save("./img-wqr1.png")


if __name__ == '__main__':
    main()

```

### Transfer

[github](https://github.com/mile-core/mile-csa-python/tree/master/examples/transfer_example.py)

```python
from milecsa import Transfer, Wallet
import time


def main():

    src = Wallet(phrase="Some WTF!? secret phrase")
    print(src.public_key, src.private_key)

    dst = Wallet()

    dst_public_key = Wallet().public_key

    state = src.get_state()

    trx0 = Transfer(src=src, dest=dst, asset_code=1, amount=0.001)
    trx1 = Transfer(src=src, dest=dst_public_key, asset_code=1, amount=1)

    print(trx0.data)
    print(trx1.data)

    #
    # Put your address
    #
    src = Wallet(phrase="secret-phrase")

    print(src.public_key, src.private_key)

    #
    # Put your address
    #
    dst = Wallet(phrase="destination-secret-phrase")

    result = src.transfer(dest=dst, asset_code=0, amount=0.1, description="give my money back!")

    print(result)

    time.sleep(21)

    state = dst.get_state()
    for b in state.balances:
        print(b)


if __name__ == "__main__":
    main()

```


### Do XDR Emission

[github](https://github.com/mile-core/mile-csa-python/tree/master/examples/emission_example.py)

```python
from milecsa import Wallet
import time


def main():
    #
    # Put your address
    #
    wallet = Wallet(private_key="...")

    result = wallet.emission(asset_code=1)

    print(result)

    time.sleep(42)

    state = wallet.get_state()
    for b in state.balances:
        print(b)

```


### Explore blocks

[github](https://github.com/mile-core/mile-csa-python/tree/master/examples/emission_example.py)

```python
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

```