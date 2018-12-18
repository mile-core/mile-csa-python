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
