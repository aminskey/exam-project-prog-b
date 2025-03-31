import requests
import json

url = "http://localhost:5000/rpc"

def call_rpc(method_name):
    payload = {
        "jsonrpc": "2.0",
        "method": method_name,
        "id": 1
    }

    headers = {'Content-type': 'application/json'}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        response_json = response.json()

        if "error" in response_json:
            print(f"RPC Error: {response_json['error']}")
            return None
        elif "result" in response_json:
            return response_json["result"]
        else:
            print("Invalid JSON-RPC response format")
            return None
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect....")
        return None
    except requests.exceptions.RequestException as e:
        print(f"An error occured during the request: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response from server: {e}")
        return None

res = call_rpc("hello")
if res is not None:
    print(res)