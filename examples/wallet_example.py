from milecsa import Wallet, config


def main():

    config.web.url = "https://wallet.testnet.mile.global"
    config.rpcDebug = True

    wallet0 = Wallet()

    wallet1 = Wallet(phrase="secret-phrase")

    wallet2 = Wallet(phrase="secret-phrase")

    wallet3 = Wallet(public_key=wallet0.public_key, private_key=wallet0.private_key)

    wallet4 = Wallet(private_key=wallet3.private_key)

    print(wallet0.public_key, wallet0.private_key)
    print(wallet1.public_key, wallet1.private_key)
    print(wallet3.public_key, wallet3.private_key)
    print(wallet4.public_key, wallet4.private_key)

    print(wallet0 == wallet2)
    print(wallet0 == wallet3)
    print(wallet1 == wallet2)
    print(wallet3 == wallet4)

    state = wallet3.get_state()

    print(state.preferred_transaction_id)

    for b in state.balances:
        print(b)


if __name__ == "__main__":
    main()
