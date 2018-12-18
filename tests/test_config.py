import unittest
from pprint import pprint
from milecsa import config


class MyTestCase(unittest.TestCase):

    def test_something(self):
        try:
            config.appSchema = ""
        except config.ConstantError as error:
            print("Constant error:", error, "\n\n")

        print("Config.nodes_urls: ", config.web.nodes_urls(), "\n")
        print("Config[]: ")
        pprint(config.__dict__)
        print()
        pprint(config.web.__dict__)
        print()
        pprint(config.web.wallet.__dict__)
        print()
        pprint(config.web.payment.__dict__)


if __name__ == '__main__':
    unittest.main()
