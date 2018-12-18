import json

import requests
import urllib3

from .config import config

urllib3.disable_warnings()


class Response:

    def __init__(self, result, id):
        self.result = result
        self.id = id
        if config.rpcDebug:
            print("Rpc Response debug: ")
            print("Id: ", id)
            print("Response: ", result)

    def __eq__(self, other):
        return (other.result == self.result) and (other.id == self.id)


class Rpc:

    headers = {'content-type': 'application/json'}
    __urls = None
    __current_url_index = 0
    __path = "/v" + config.version + "/api"

    def __init__(self, method, params):
        self.id = 0
        self.__payload = {
            "method": method,
            "params": params,
            "jsonrpc": "2.0",
            "id": self.id,
        }

    @classmethod
    def get_url(cls):

        if config.useBalancing:
            if not cls.__urls:
                cls.__urls = requests.get(
                    config.web.nodes_urls(),
                    verify=config.sslVerification,
                    timeout=config.connectionTimeout
                ).json()

            cls.__current_url_index += 1
            return cls.__urls[cls.__current_url_index % len(cls.__urls)] + cls.__path
        else:
            return config.url + cls.__path

    def exec(self):

        self.__payload["id"] = self.id
        data = json.dumps(self.__payload)
        self.id += 1

        if config.rpcDebug:
            print("Rpc exec debug: ")
            print(data)

        response = requests.post(
            self.get_url(),
            data=data,
            headers=self.headers,
            timeout=config.connectionTimeout,
            verify=config.sslVerification,
            stream=False
        ).json()

        error = response.get('error', None)
        if error:
            if config.rpcDebug:
                print("Rpc error debug: ")
                print(error)
            raise Exception(error['message'])

        return Response(response['result'], response["id"])
