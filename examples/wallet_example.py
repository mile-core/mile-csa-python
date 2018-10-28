from milecsa import Wallet, Config


def main():

    Config.url = "http://wallet.testnet.mile.global"

    wallet0 = Wallet()

    wallet1 = Wallet(phrase="secret-phrase")

    wallet2 = Wallet(phrase="secret-phrase")

    wallet3 = Wallet(public_key=wallet0.publicKey, private_key=wallet0.privateKey)

    wallet4 = Wallet(private_key=wallet3.privateKey)

    print(wallet0.publicKey, wallet0.privateKey)
    print(wallet1.publicKey, wallet1.privateKey)
    print(wallet3.publicKey, wallet3.privateKey)
    print(wallet4.publicKey, wallet4.privateKey)

    print(wallet0 == wallet2)
    print(wallet0 == wallet3)
    print(wallet1 == wallet2)
    print(wallet3 == wallet4)

    state = wallet3.get_state()

    print(state.last_transaction_id)

    for b in state.balances:
        print(b)


if __name__ == "__main__":
    main()
