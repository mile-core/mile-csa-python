import unittest
from milecsa import Chain, Config
from .local_config import *


class MyTestCase(unittest.TestCase):
    def test_something(self):

        chain0 = Chain()

        chain1 = Chain()

        print(chain0.project,
              chain0.version,
              chain0.supported_transactions,
              chain0.asset_codes,
              chain0.asset_names)

        print("Last block id: ", chain1.get_current_block_id())

        self.assertEqual(chain0, chain1)


if __name__ == '__main__':
    unittest.main()
