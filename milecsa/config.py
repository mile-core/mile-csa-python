
class Constant:

    __excludes__ = []

    class ConstantError(Exception):
        pass

    def __setattr__(self, name, value):

        exclude = name in Constant.__excludes__

        if self.__dict__.get(name, None) and not exclude:
            raise Constant.ConstantError("Property %s is not mutable" % name)

        self.__dict__[name] = value


class Config(Constant):

    def __init__(self):

        Constant.__excludes__.append('sslVerification')
        Constant.__excludes__.append('connectionTimeout')
        Constant.__excludes__.append('url')
        Constant.__excludes__.append('useBalancing')
        Constant.__excludes__.append('rpcDebug')

        self.version = "1"
        self.url = "https://wallet.mile.global"
        self.appSchema = "mile-core:"
        self.sslVerification = True
        self.connectionTimeout = 30
        self.useBalancing = True
        self.rpcDebug = False

        self.web = self.Web(self)

    class Web(Constant):
        def __init__(self, config):
            self.path = "shared"
            self.url = "https://wallet.mile.global"

            self.config = config
            self.wallet = self.Wallet(self)
            self.payment = self.Payment(self)

        def nodes_urls(self):
            return self.url + "/v" + self.config.version + "/nodes.json"

        def base_url(self):
            return self.url + "/v" + self.config.version

        class Wallet(Constant):
            def __init__(self, web):
                self.web = web

                self.public_key = "/" + self.web.path + "/wallet/key/public/"
                self.private_key = "/" + self.web.path + "/wallet/key/private/"
                self.note = "/" + self.web.path + "/wallet/note/"
                self.name = "/" + self.web.path + "/wallet/note/name/"
                self.secret_phrase = "/" + self.web.path + "/wallet/secret/phrase/"
                self.amount = "/" + self.web.path + "/wallet/amount/"

        class Payment:
            def __init__(self, web):
                self.web = web

                self.public_key = "/" + self.web.path + "/payment/key/public/"
                self.amount = "/" + self.web.path + "/payment/amount/"


config = Config()
