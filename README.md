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

**Global configuration**
```python
from milecsa.Config import Config

#
# disable SSL verification
#
Config.sslVerification = False

#
# set up user defined connection timeout
#
Config.connectionTimeout = 30 # seconds

#
# use MILE testnet 
#
Config.url = "https://wallet.testnet.mile.global"

```

**Wallet create**
```python
from milecsa.Wallet import Wallet


def main():

    wallet0 = Wallet(phrase="Some phrase")

    print(wallet0.publicKey, wallet0.privateKey)

    #
    # Put your address
    #
    wallet1 = Wallet(public_key="...")

    state = wallet1.get_state()
    print(state.balances, state.last_transaction_id, wallet1.publicKey)
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

**Send transfer**
```python
from milecsa import Transfer, Wallet
import time


def main():

    src = Wallet(phrase="Some WTF!? secret phrase")
    print(src.publicKey, src.privateKey)

    dst = Wallet()

    dst_public_key = Wallet().publicKey

    state = src.get_state()

    trx0 = Transfer(src=src, dest=dst, asset=1, amount=0.001)
    trx1 = Transfer(src=src, dest=dst_public_key, asset=1, amount=10)

    print(trx0.data)
    print(trx1.data)

    #
    # Put your address
    #
    src = Wallet(private_key="...")

    print(src.publicKey, src.privateKey)

    #
    # Put your address
    #
    dst = Wallet(public_key="...")

    result = src.transfer(dest=dst, asset=1, amount=1)

    print(result)

    time.sleep(60)

    state = dst.get_state()
    for b in state.balances:
        print(b)



if __name__ == "__main__":
    main()
```

**Do XDR Emission**
```python
from milecsa import Transfer, Wallet
import time

def main():
    #
    # Put your address
    #
    src = Wallet(private_key="...")

    #
    # Put your address
    #
    dst = Wallet(public_key="...")

    result = src.emission(dest=dst, asset=1, amount=1000)

    print(result)

    time.sleep(60)

    state = dst.get_state()
    for b in state.balances:
        print(b)

```

**Explore blocks**

```python
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
    Config.url = "http://node002.testnet.mile.global"
    #
    # Disable client balancing
    #
    Config.useBalancing = False

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