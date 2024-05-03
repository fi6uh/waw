import requests
import subprocess
import json
import os


class WWWHost:
    def __init__(self, headers, url):
        self.headers = headers
        self.base_url = url

    def endpoint_builder(self, endpoint, params):
        url = self.base_url + endpoint
        if len(params) > 0:
            url += '?'
            for param in params.keys():
                url += param + '=' + str(params[param]) + '&'
            url = url[:-1]
        return url

    def simple_req(self, method, endpoint, params, payload={}):
        url = self.endpoint_builder(endpoint, params)
        response = requests.request(method.upper(), url, headers=self.headers, data=payload)
        return response


class Headers:
    def __init__(self, token=None):
        self.headers = {
            "User-Agent": "WaW Tool",
            "Content-Type": "application/json",
            "Accepts": "application/json"
        }
        if token is not None:
            self.headers["Authorization"] = "Bearer " + token


class API:
    def __init__(self, config_path):
        self.path = config_path
        self.config = self.read()
        token = None
        if "auth" in self.config.keys():
            token = self.config["auth"]
        host = self.config["host"]
        headers = Headers(token)
        self.client = WWWHost(headers.headers, host)

    def read(self):
        data = {}
        if os.path.exists(self.path):
            with open(self.path, 'r') as fh:
                data = json.load(fh)
        return data

    def call(self, function, parameters={}):
        if function in self.config["endpoints"].keys():
            method = self.config["endpoints"][function]["method"]
            endpoint = self.config["endpoints"][function]["endpoint"]
            response = self.client.simple_req(method, endpoint, parameters)
            return response


def main():
    test = "examples/test.json"
    api = API(test)
    data = api.call("home")
    print(data.text[:100])


if __name__ == "__main__":
    main()
