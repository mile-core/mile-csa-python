import milecsa


class TransactionParser:

    def parse(self, json_data, block_id=None):
        res = []

        tx_type = json_data['transaction-type']
        tx_id=json_data['transaction-id']

        if tx_type == 'TransferAssetsTransaction':
            for a in json_data['asset']:
                asset_code = int(a['code'])
                amount = a['amount']

                tx = milecsa.Transfer(
                    src=json_data['from'],
                    dest=json_data['to'],
                    asset_code=asset_code,
                    amount=amount,
                    description=json_data["description"],
                    fee=json_data['fee'],
                    tx_id=tx_id,
                    block_id=block_id
                )

                res.append(tx)
        elif tx_type == 'EmissionTransaction':
            tx = milecsa.Emission(
                wallet=json_data['from'], asset_code=int(json_data['code']),
                fee=json_data['fee'], tx_id=tx_id, block_id=block_id
            )
            res.append(tx)
        elif tx_type == 'RegisterNodeTransactionWithAmount':
            tx = milecsa.RegisterNode(
                wallet=json_data['public-key'],
                address=json_data['address'],
                amount=json_data['amount'],
                tx_id=tx_id,
                block_id=block_id
            )
            res.append(tx)
        elif tx_type == 'UnregisterNodeTransaction':
            tx = milecsa.UnregisterNode(
                wallet=json_data['public-key'],
                tx_id=tx_id,
                block_id=block_id
            )
            res.append(tx)
        elif tx_type == 'PostTokenRate':
            tx = milecsa.PostTokenRate(
                wallet=json_data['public-key'],
                rate=json_data['course'],
                tx_id=tx_id,
                block_id=block_id
            )
            res.append(tx)

        return res
