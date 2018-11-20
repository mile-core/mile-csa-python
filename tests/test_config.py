import unittest
from pprint import pprint
from milecsa import Config


class MyTestCase(unittest.TestCase):

    def test_something(self):
        try:
            Config.appSchema = ""
        except Config.ConstantError as error:
                print("Constant error:", error)

        print("Config.nodesUrl: ", Config.nodesUrl())
        print("Config[]: ")
        pprint(Config.__dict__)
        pprint(Config.Shared.__dict__)
        pprint(Config.Shared.Wallet.__dict__)
        pprint(Config.Shared.Payment.__dict__)


if __name__ == '__main__':
    unittest.main()
