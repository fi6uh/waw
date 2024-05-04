# Web-application Wrapper (WaW)

WaW is a lightweight Python tool designed to simplify web requests to various APIs. It allows you to interact with APIs using easy-to-understand Python code, abstracting away much of the complexity involved in making HTTP requests.

## Features

- **Simplified API Interaction**: WaW reads API definitions from JSON files, making it easy to define endpoints and their corresponding methods.
- **Automatic Header Handling**: You can specify custom headers, including authentication tokens, which are automatically included in your requests.
- **Dynamic Endpoint Building**: Easily construct API endpoints with dynamic parameters, simplifying URL construction.
- **Debugging Support**: Debugging responses is made straightforward with built-in support for printing request and response details.

## How to Use

- **Define API Configurations**: Create JSON files specifying API configurations, including endpoints, methods, and optional authentication details.
- **Initialize API**: Initialize the API class with the path to your JSON configuration file.
- **Make Requests**: Use the call method of the API instance to make requests to defined endpoints, optionally passing parameters and URL arguments.
- **Debug Responses (Optional)**: For debugging purposes, utilize the Debug class to print detailed information about request and response objects.

### Example

API spec:

```
{
  "host": "https://stackoverflow.com",
  "endpoints": {
    "questions": {
      "method": "GET",
      "endpoint": "/questions/{qid}/{title}"
    }
  }
}
```

Python:

```
import API

# initialize the API
test = "examples/so.json"
api = API(test)

# our endpoint takes path parameters
first_so_question = {
    "qid": 4,
    "title": "how-to-convert-decimal-to-double-in-c"
}
data = api.call("questions", url_params=first_so_question)

# print request and response metadata
debugger = Debug(data)
print(debugger)
```
