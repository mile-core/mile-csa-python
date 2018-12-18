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
