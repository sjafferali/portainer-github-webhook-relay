import requests
import datetime
import json
import traceback
from cfg import TOKEN_EXPIRATION, STACK_CACHE_EXPIRATION

TIMEOUT = 60


class Portainer:
    def __init__(self, portainer_endpoint, username, password, verify=True):
        self.portainer_endpoint = portainer_endpoint+"/api"
        self.username = username
        self.password = password
        self.verify_ssl = verify
        self.token_expiration = None
        self.token = None
        self.stack_cache_expiration = None
        self.stack_cache = None

    def get_token(self):
        if self.token and datetime.datetime.now() < self.token_expiration:
            print("got token from cache")
            return self.token

        print("authenticating")
        response = self.make_request(
            self.portainer_endpoint+"/auth",
            "POST",
            False,
            {"Username": self.username, "Password": self.password}
        )
        if response:
            self.token = response.get("jwt")
            self.token_expiration = datetime.datetime.now() + datetime.timedelta(seconds=TOKEN_EXPIRATION)

        return self.token

    def make_request(self, url, method, auth_header=True, body=None):
        if body is not None:
            body = json.dumps(body)

        headers = {"Content-Type": "application/json"}
        if auth_header:
            token = self.get_token()
            if not token:
                return None
            headers["Authorization"] = f"Bearer {token}"

        try:
            r = requests.request(method, headers=headers, url=url, data=body, timeout=TIMEOUT, verify=self.verify_ssl)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print("Http Error:", e)
            return None
        except requests.exceptions.ConnectionError as e:
            print("Error Connecting:", e)
            return None
        except requests.exceptions.Timeout as e:
            print("Timeout Error:", e)
            return None
        except requests.exceptions.RequestException as e:
            print("OOps: Something Else", e)
            return None

        try:
            json_response = r.json()
        except Exception as e:
            print(f"Error occurred converting response to json {e}")
            #traceback.print_exc()
            return r.text

        return json_response

    def get_stacks(self):
        if self.stack_cache and datetime.datetime.now() < self.stack_cache_expiration:
            print("got stack list from cache")
            return self.stack_cache

        print("getting stack list")
        url = self.portainer_endpoint + "/stacks"
        response = self.make_request(url=url, method="GET", auth_header=True)
        if response:
            self.stack_cache = response
            self.stack_cache_expiration = datetime.datetime.now() + datetime.timedelta(seconds=STACK_CACHE_EXPIRATION)

        return self.stack_cache

    def stack_webhook(self, webhook):
        # https: // portainer.home.samir.network/api/stacks/webhooks/f67b9bf3-e03a-49f4-a2b2-9cae81f39039
        url = f"{self.portainer_endpoint}/stacks/webhooks/{webhook}"
        return self.make_request(url=url, method="POST", auth_header=False, body={})


class Stack:
    def __init__(self, name, git_url, git_configfile, git_ref, webhook):
        self.webhook = webhook
        self.name = name
        self.git_url = git_url
        self.git_configfile = git_configfile
        self.git_ref = git_ref
