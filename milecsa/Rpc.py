from milecsa.Config import Config
import requests
import json
import urllib3

urllib3.disable_warnings()


class Response:

    def __init__(self, result, id):
        self.result = result
        self.id = id
        if Config.rpcDebug:
            print("Rpc Response debug: ")
            print("Id: ", id)
            print("Response: ", result)

    def __eq__(self, other):
        return (other.result == self.result) and (other.id == self.id)


class Rpc:

    headers = {'content-type': 'application/json'}
    __urls__ = None
    __current__url__index__ = 0

    def __init__(self, method, params):

        self.id = 0

        self.__payload = {
            "method": method,
            "params": params,
            "jsonrpc": "2.0",
            "id": self.id,
        }

        if Config.useBalancing and not Rpc.__urls__:
            Rpc.__urls__ = requests.get(Config.nodesUrl()).json()

    @staticmethod
    def get_url():
        target = "/v"+Config.version+"/api"
        if Config.useBalancing:
            Rpc.__current__url__index__ += 1
            return Rpc.__urls__[Rpc.__current__url__index__ % len(Rpc.__urls__)]+target
        else:
            return Config.url+target

    def exec(self):

        self.__payload["id"] = self.id
        data = json.dumps(self.__payload)
        self.id += 1

        if Config.rpcDebug:
            print("Rpc exec debug: ")
            print(data)

        response = requests.post(
            self.get_url(),
            data=data,
            headers=self.headers,
            timeout=Config.connectionTimeout,
            verify=Config.sslVerification,
            stream=False).json()

        error = response.get('error', None)
        if error:
            if Config.rpcDebug:
                print("Rpc error debug: ")
                print(error)
            raise Exception(error['message'])

        return Response(response['result'], response["id"])
