from milecsa import Transfer, Wallet, config
import time


def main():

    config.web.url = "https://wallet.testnet.mile.global"

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
