import base64
import json
import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from requests import Response


class Authenticate:
    load_dotenv()

    def __init__(self,
                 scope: str = 'product.compact'):
        self.client_id = os.environ.get('CLIENT_ID')
        self.client_secret = os.environ.get('CLIENT_SECRET')
        self.auth_token = f"{self.client_id}:{self.client_secret}".encode("ascii")
        self.oauth_connect_uri = os.environ.get('OAUTH_CONNECT_URI')
        self.access_token = os.environ.get('ACCESS_TOKEN')
        self.expires_in = os.environ.get('EXPIRES_IN')
        self.scope = scope

    def get_auth_access_token(self,
                              write_to_env_file: bool = False):
        if self.__is_token_still_valid():
            return self.access_token
        auth_resp = self.post_oauth()
        if auth_resp.status_code != 200:
            raise Exception(f"Bad request:\n{auth_resp.reason}")
        auth_dict = json.loads(auth_resp.content)
        if write_to_env_file:
            self.__write_new_token_to_env_file(auth_dict)
        else:
            self.access_token = auth_dict['access_token']
            return self.access_token

    def post_oauth(self) -> Response:
        encoded_token = base64.b64encode(self.auth_token)
        encoded_string = encoded_token.decode('ascii')
        try:
            return requests.post(self.oauth_connect_uri,
                                 headers={
                                     "Authorization": f"Basic {encoded_string}",
                                     "Content-Type": "application/x-www-form-urlencoded"
                                 },
                                 data={
                                     "grant_type": "client_credentials",
                                     "scope": self.scope
                                 })
        except Exception as e:
            raise Exception(f"Something went wrong when authenticating:\n{e}")

    def __is_token_still_valid(self) -> bool:
        if self.access_token:
            if self.expires_in:
                now = datetime.utcnow()
                old_expiration_time_string = datetime.fromisoformat(self.expires_in)
                return now <= old_expiration_time_string
        return False

    def __write_new_token_to_env_file(self, auth_response: dict):
        access_token = auth_response['access_token']
        expires_in_seconds = auth_response['expires_in']
        expiration_time = (datetime.utcnow() + timedelta(seconds=expires_in_seconds)).isoformat()
        with open('.env', 'r') as f:
            lines = f.readlines()
        with open('.env', 'w') as f:
            for line in lines:
                if 'ACCESS_TOKEN' not in line and 'EXPIRES_IN' not in line:
                    f.write(line)
                elif 'ACCESS_TOKEN' in line:
                    f.write(f"ACCESS_TOKEN={access_token}\n")
                    self.access_token = access_token
                elif 'EXPIRES_IN' in line:
                    f.write(f"EXPIRES_IN={expiration_time}")
