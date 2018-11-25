import milecsa  # todo


class TransactionParser:

    def __init__(self, json_data):
        self.transactions = []
        tx_type = json_data['transaction-type']

        if tx_type in ['TransferAssetsTransaction', 'EmissionTransaction']:

            assets = json_data['asset']
            frm = json_data['from']
            to = json_data['to']
            tx_id = json_data['transaction-id']
            description = json_data["description"]

            for a in assets:
                asset_code = int(a['code'])
                amount = a['amount']

                # if type(asset_code) is str:
                #    asset = self.__chain.asset_code(name=asset)

                if tx_type == 'TransferAssetsTransaction':
                    trx = milecsa.Transfer(
                        src=frm, dest=to, asset_code=asset_code, amount=amount, description=description, tx_id=tx_id
                    )

                elif tx_type == 'EmissionTransaction':
                    trx = milecsa.Emission(
                        src=frm, dest=to, asset_code=asset_code, amount=amount, description=description, tx_id=tx_id
                    )

                else:
                    continue

                self.transactions.append(trx)
