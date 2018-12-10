import __milecsa as milecsa


def main():
    print(dir(milecsa))
    print()

    try:
        print("1.0 Generate key")
        pk = milecsa.__key_pair()
        print(pk)

        print()

        print("1.1 Generate public key by private")

        pkp = pk['private-key']
        print(milecsa.__key_pair_from_private_key(pkp))

    except Exception as error:
        print(error)


    print()

    try:

        print("2. Generate key by secret phrase")
        pk1 = milecsa.__key_pair_with_secret_phrase("The some phrase")
        pk2 = milecsa.__key_pair_with_secret_phrase("The some phrase")

        pk3 = milecsa.__key_pair_with_secret_phrase("The some new phrase")

        print(pk1, pk1 == pk2, pk1 == pk3)

    except Exception as error:
        print(error)


    print()

    try:

        print("3. Create signed transfer transaction")
        print(milecsa.__transfer_assets(pk1['public-key'],
                                        pk1['private-key'],
                                        pk3["public-key"],
                                        0,    # block id
                                        1,    # trx id
                                        0,    # asset code
                                        20,   # amount
                                        0.0,  # fee
                                        ''  # memo
                                        ))

        print()

        print("4. Create signed emission transaction")
        print(milecsa.__emission(pk1['public-key'],
                                        pk1['private-key'],
                                        0,  # block id
                                        1,  # trx id
                                        0,  # asset code
                                        0   # fee
                                        ))

        print()

        print("4. Generate signed register node transaction")
        print(milecsa.__register_node(pk1['public-key'],
                                      pk1['private-key'],
                                      "mile.global",  # node address
                                      0,      # block id
                                      0,      # trx id
                                      10,     # amount
                                      0,      # fee
                                      ))

        print()

        print("5. Generate signed unregister node transaction")
        print(milecsa.__unregister_node(pk1['public-key'],
                                        pk1['private-key'],
                                        0,  # block id
                                        0,  # trx id
                                        0  # fee
                                        ))

    except Exception as error:
        print(error)


    print()

    try:
        print("7. Test exception")

        print(milecsa.__transfer_assets(pk1['public-key'], pk1['private-key'], pk3["public-key"], 0, 1, 1, "20"))
    except Exception as error:
        print(error)


if __name__ == "__main__":
    main()
