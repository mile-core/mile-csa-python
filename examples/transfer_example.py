from milecsa import Transfer, Wallet, Config
import time


def main():

    Config.url = "https://wallet.testnet.mile.global"

    src = Wallet(phrase="Some WTF!? secret phrase")
    print(src.publicKey, src.privateKey)

    dst = Wallet()

    dst_public_key = Wallet().publicKey

    state = src.get_state()

    trx0 = Transfer(src=src, dest=dst, asset_code=1, amount=0.001)
    trx1 = Transfer(src=src, dest=dst_public_key, asset_code=1, amount=1)

    print(trx0.data)
    print(trx1.data)

    #
    # Put your address and
    #
    src = Wallet(phrase="secret-phrase")

    print(src.publicKey, src.privateKey)

    #
    # Put your address and
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
