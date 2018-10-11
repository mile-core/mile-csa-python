
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

        self.Shared = self.Shared(self)


    def nodesUrl(self):
        return self.api() + "/v" + self.version + "/nodes.json"

    def baseUrl(self):
        return self.api() + "/v" + self.version

    def api(self):
        return self.url

    class Shared(Constant):

        path = "shared"

        def __init__(self, config):
            self.Config = config
            self.Wallet = self.Wallet(self)
            self.Payment = self.Payment(self)

        class Wallet(Constant):

            def __init__(self, shared):
                self.Shared = shared
                self.publicKey = "/" + self.Shared.path + "/wallet/key/public/"
                self.privateKey = "/" + self.Shared.path + "/wallet/key/private/"
                self.note = "/" + self.Shared.path + "/wallet/note/"
                self.name = "/" + self.Shared.path + "/wallet/note/name/"
                self.secretPhrase = "/" + self.Shared.path + "/wallet/secret/phrase/"
                self.amount = "/" + self.Shared.path + "/wallet/amount/"

        class Payment:

            def __init__(self, shared):
                self.Shared = shared
                self.publicKey = "/" + self.Shared.path + "/payment/key/public/"
                self.amount = "/" + self.Shared.path + "/payment/amount/"


Config = Config()
