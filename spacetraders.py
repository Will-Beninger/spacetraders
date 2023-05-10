import os
import requests
import pandas as pd

class APIRequester:
    def __init__(self, base_url):
        self.base_url = base_url

    def print_urls(self):
        return

    def send_request(self, endpoint, method='GET', data=None):
        url = f"{self.base_url}/{endpoint}"
        if method == 'GET':
            response = requests.get(url)
        elif method == 'POST':
            response = requests.post(url, data=data)
        else:
            raise ValueError("Invalid HTTP method. Allowed values: 'GET' or 'POST'.")

        return response

if __name__ == '__main__':
    #Initialize the authorization token:
    
    #Create new API Requester:
    requester = APIRequester('https://api.spacetraders.io/v2')

    while True:
        print("Please select an endpoint:")
        print("1. /my/agent")
        print("2. /comments")
        print("3. /albums")
        print("4. /photos")
        print("5. /todos")
        print("6. /users")
        endpoint_choice = input("> ")

        if endpoint_choice == '1':
            endpoint = 'posts'
        elif endpoint_choice == '2':
            endpoint = 'comments'
        elif endpoint_choice == '3':
            endpoint = 'albums'
        elif endpoint_choice == '4':
            endpoint = 'photos'
        elif endpoint_choice == '5':
            endpoint = 'todos'
        elif endpoint_choice == '6':
            endpoint = 'users'
        else:
            print("Invalid choice. Please try again.")
            continue

        print("Please select an HTTP method:")
        print("1. GET")
        print("2. POST")
        method_choice = input("> ")

        if method_choice == '1':
            method = 'GET'
        elif method_choice == '2':
            method = 'POST'
        else:
            print("Invalid choice. Please try again.")
            continue

        if method == 'POST':
            data = {}
            while True:
                key = input("Enter a key for the data (leave blank to finish): ")
                if not key:
                    break
                value = input(f"Enter a value for the key '{key}': ")
                data[key] = value
        else:
            data = None

        response = requester.send_request(endpoint, method=method, data=data)

        if 'application/json' in response.headers['Content-Type']:
            # If the response content type is JSON, parse it into a table
            df = pd.read_json(response.text)
            print(df)
        else:
            # Otherwise, just print the response body
            print(f"Response code: {response.status_code}")
            print("Response body:")
            print(response.text)
