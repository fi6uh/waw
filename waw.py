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
            token = os.environ.get(self.config["auth"])
        host = self.config["host"]
        headers = Headers(token)
        self.client = WWWHost(headers.headers, host)

    def read(self):
        data = {}
        if os.path.exists(self.path):
            with open(self.path, 'r') as fh:
                data = json.load(fh)
        return data

    def call(self, function, parameters={}, url_args={}):
        if function in self.config["endpoints"].keys():
            method = self.config["endpoints"][function]["method"]
            endpoint = self.config["endpoints"][function]["endpoint"]
            if "{" in endpoint and "}" in endpoint:
                endpoint = endpoint.format(**url_args)
            response = self.client.simple_req(method, endpoint, parameters)
            return response


class Debug:
    def __init__(self, response):
        self.response = response
        self.request = response.request

    def get_obj_data(self, obj):
        cookies = {}
        if "cookies" in obj.__dict__.keys():
            cookies = obj.cookies
        else:
            cookies = obj._cookies
        cookies = cookies.get_dict()
        data = {
            "url" : obj.url,
            "headers" : dict(obj.headers),
            "cookies" : dict(cookies)
        }
        return data

    def __str__(self):
        code = self.response.status_code
        request = self.get_obj_data(self.request)
        response = self.get_obj_data(self.response)
        debug = {
            "request": request,
            "response": response,
            "status": code
        }
        return json.dumps(debug, indent=2)


def main():
    test = "examples/so.json"
    api = API(test)

    first_so_question = {
        "qid": 4,
        "title": "how-to-convert-decimal-to-double-in-c"
    }
    data = api.call("questions", url_args=first_so_question)

    debugger = Debug(data)
    print(debugger)


if __name__ == "__main__":
    main()
