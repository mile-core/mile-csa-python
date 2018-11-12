import milecsa


class TransactionParser:

    def __init__(self, json_data):
        self.transactions = []
        trx_type = json_data['transaction-type']

        if trx_type in ['TransferAssetsTransaction', 'EmissionTransaction']:

            _assets = json_data['asset']
            frm = json_data['from']
            to = json_data['to']
            trxId = json_data['transaction-id']
            description = json_data["description"]

            for a in _assets:
                asset_code = int(a['code'])
                amount = a['amount']

                # if type(asset_code) is str:
                #    asset = self.__chain.asset_code(name=asset)

                if trx_type == 'TransferAssetsTransaction':
                    trx = milecsa.Transfer(src=frm, dest=to, asset_code=asset_code, amount=amount, description=description, trxid=trxId)

                elif trx_type == 'EmissionTransaction':
                    trx = milecsa.Emission(src=frm, dest=to, asset_code=asset_code, amount=amount, description=description, trxid=trxId)

                self.transactions.append(trx)

