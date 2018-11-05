import json
import unittest

from __milecsa import __key_pair as key_pair, \
    __key_pair_with_secret_phrase as key_pair_with_secret_phrase, \
    __key_pair_from_private_key as key_pair_from_private_key, \
    __transfer_assets as transfer_assets, \
    __emission as emission, \
    __register_node as register_node, \
    __unregister_node as unregister_node

class TestBindings(unittest.TestCase):
    def test_keypair(self):
        pair = key_pair()
        self._validate_pair(pair)

    def test_key_pair_with_secret_phrase(self):
        pair1 = key_pair_with_secret_phrase("secret-phrase")
        self._validate_pair(pair1)
        pair2 = key_pair_with_secret_phrase(phrase="secret-phrase")
        self._validate_pair(pair2)

        self.assertDictEqual(pair1, pair2)
        self.assertDictEqual(
            {
                'public-key': 'eZrf8Eq1qDvSCEfdeezBRhT3QSf5GkrQH9tzGNaYt8q8gH5aZ',
                'private-key': 'XPBeWywB2XCgTVATLY5kYTTwNC5GwVqYyNcsTeLb7Mmn2KSNjTUzhxPJG88aiSWiuiXp7y7xHzCikNimmcz2a65mZgnBj'
            },
            pair1
        )


        # todo humanize errors
        self.assertRaises(TypeError, key_pair_with_secret_phrase, 1)
        self.assertRaises(TypeError, key_pair_with_secret_phrase)
        self.assertRaisesWithMessage(RuntimeError, "MileCsa error: secret phrase is empty", key_pair_with_secret_phrase, "")

    def test_key_pair_from_private_key(self):
        pair1 = key_pair()
        pair2 = key_pair_from_private_key(pair1['private-key'])
        self._validate_pair(pair2)
        self.assertDictEqual(pair1, pair2)

        pair3 = key_pair_with_secret_phrase("secret-phrase")
        pair4 = key_pair_from_private_key(private_key=pair3['private-key'])
        self._validate_pair(pair4)
        self.assertDictEqual(pair3, pair4)

        # todo humanize errors
        self.assertRaises(TypeError, key_pair_from_private_key, 1)
        self.assertRaises(TypeError, key_pair_from_private_key)
        self.assertRaisesWithMessage(RuntimeError, "MileCsa error: private key is empty", key_pair_from_private_key, "")
        self.assertRaisesWithMessage(RuntimeError, "MileCsa error: Error read private key: base58 check string decode error", key_pair_from_private_key, "incorrectprivatekey")

    def test_transfer_assets(self):
        pair1 = key_pair_with_secret_phrase("secret-phrase")
        pair2 = key_pair_with_secret_phrase("destination-secret-phrase")

        res_str = transfer_assets(
            pair1['public-key'],
            pair1['private-key'],
            pair2['public-key'],
            2**64-1,
            1,
            1,
            0.29*100,
            0.1+0.2,
            "22memo"
        )
        self.assertIs(type(res_str), str)
        res = json.loads(res_str)
        self.assertIs(type(res), dict)

        self.assertEqual('29.00000', res.get('asset', {}).get('amount', ''))
        self.assertEqual(1, res.get('asset', {}).get('code'))
        self.assertEqual("22memo", res.get('description'))
        self.assertEqual("0.30000", res.get('fee'))
        self.assertEqual(pair1['public-key'], res.get('from'))
        self.assertEqual(pair2['public-key'], res.get('to'))
        self.assertEqual(str(2**64-1), res.get('block-id'))
        self.assertEqual(1, res.get('transaction-id'))
        self.assertEqual('TransferAssetsTransaction', res.get('transaction-name'))

        # runs without memo
        res_str = transfer_assets(
            pair1['public-key'],
            pair1['private-key'],
            pair2['public-key'],
            2 ** 64 - 1,
            1,
            1,
            0.29 * 100,
            0.1 + 0.2
        )
        self.assertIs(type(res_str), str)
        res = json.loads(res_str)
        self.assertIs(type(res), dict)
        self.assertEqual("", res.get('description'))

    def test_emission(self):
        pair = key_pair_with_secret_phrase("secret-phrase")

        res_str = emission(
            pair['public-key'], pair['private-key'],
            2**64-1, 1,
            1, 0.1+0.2
        )
        self.assertIs(type(res_str), str)
        res = json.loads(res_str)
        self.assertIs(type(res), dict)

        self.assertEqual(1, res.get('asset', {}).get('code'))
        self.assertEqual("0.30000", res.get('fee'))
        self.assertEqual(pair['public-key'], res.get('from'))
        self.assertEqual(str(2**64-1), res.get('block-id'))
        self.assertEqual(1, res.get('transaction-id'))
        self.assertEqual('EmissionTransaction', res.get('transaction-name'))

    def test_register_node(self):
        pair = key_pair_with_secret_phrase("secret-phrase")

        res_str = register_node(
            pair['public-key'], pair['private-key'],
            '127.0.0.2',
            2**64-1, 1,
            1, 0.1+0.2
        )
        self.assertIs(type(res_str), str)
        res = json.loads(res_str)
        self.assertIs(type(res), dict)

        self.assertEqual('127.0.0.2', res.get('address'))
        self.assertEqual(1, res.get('asset', {}).get('code'))
        self.assertEqual('0.30000', res.get('asset', {}).get('amount'))
        self.assertEqual(pair['public-key'], res.get('public-key'))
        self.assertEqual(str(2**64-1), res.get('block-id'))
        self.assertEqual(1, res.get('transaction-id'))
        self.assertEqual('RegisterNodeTransactionWithAmount', res.get('transaction-name'))

    def test_unregister_node(self):
        pair = key_pair_with_secret_phrase("secret-phrase")

        res_str = unregister_node(
            pair['public-key'], pair['private-key'],
            '127.0.0.2',
            2**64-1, 1
        )
        self.assertIs(type(res_str), str)
        res = json.loads(res_str)
        self.assertIs(type(res), dict)

        # todo self.assertEqual('127.0.0.2', res.get('address'))
        self.assertEqual(pair['public-key'], res.get('public-key'))
        self.assertEqual(str(2**64-1), res.get('block-id'))
        self.assertEqual(1, res.get('transaction-id'))
        self.assertEqual('UnregisterNodeTransaction', res.get('transaction-name'))

    def _validate_pair(self, pair):
        self.assertIs(type(pair), dict)
        self.assertIn('private-key', pair)
        self.assertIn('public-key', pair)
        self.assertIs(type(pair['private-key']), str)
        self.assertIs(type(pair['public-key']), str)
        self.assertNotEqual("", pair['private-key'])
        self.assertNotEqual("", pair['public-key'])

    def assertRaisesWithMessage(self, exception_type, msg: str, func, *args, **kwargs):
        self.assertNotEqual("", msg, "Message can't be empty")
        try:
            func(*args, **kwargs)
            self.fail(f"Exception {exception_type.__name__} was not raised")
        except Exception as e:
            if type(e) is not exception_type:
                self.fail(f"Exception {exception_type.__name__} was not raised")
            self.assertIn(msg, str(e))


if __name__ == '__main__':
    unittest.main()
