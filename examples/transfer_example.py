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
    # Put your address and
    #
    src = Wallet(private_key="...")

    print(src.publicKey, src.privateKey)

    #
    # Put your address and
    #
    dst = Wallet(public_key="...")

    result = src.transfer(dest=dst, asset=1, amount=1, description="give my money back!")

    print(result)

    time.sleep(60)

    state = dst.get_state()
    for b in state.balances:
        print(b)


if __name__ == "__main__":
    main()
