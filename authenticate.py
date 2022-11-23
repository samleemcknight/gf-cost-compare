import os
from datetime import datetime, timedelta
from typing import Dict

from dotenv import load_dotenv
import requests
import base64
import json


class Authenticate:
    load_dotenv()

    def __init__(self,
                 scope: str = 'product.compact'):
        self.client_id = os.environ.get('CLIENT_ID')
        self.client_secret = os.environ.get('CLIENT_SECRET')
        self.auth_token = f"{self.client_id}:{self.client_secret}".encode("ascii")
        self.oauth_connect_uri = os.environ.get('OAUTH_CONNECT_URI')
        self.access_token = os.environ.get('ACCESS_TOKEN')
        self.scope = scope

    def get_auth_access_token(self):
        encoded_token = base64.b64encode(self.auth_token)
        encoded_string = encoded_token.decode('ascii')
        now = datetime.utcnow()

        with open('.env', 'r') as f:
            lines = f.readlines()

        old_expires_in = [line for line in lines if 'EXPIRES_IN' in line]
        old_expiration_time_string = datetime.fromisoformat(old_expires_in[0].split('=')[1].replace('\n', ''))

        if now >= old_expiration_time_string:
            auth_resp = requests.post(self.oauth_connect_uri,
                                      headers={
                                          "Authorization": f"Basic {encoded_string}",
                                          "Content-Type": "application/x-www-form-urlencoded"
                                      },
                                      data={
                                          "grant_type": "client_credentials",
                                          "scope": self.scope
                                      })

            if auth_resp.status_code != 200:
                raise Exception(f"Something went wrong when authenticating:\n{auth_resp.reason}")
            auth_response = json.loads(auth_resp.content)
            access_token = auth_response['access_token']
            expires_in_seconds = auth_response['expires_in']
            EXPIRATION_TIME = (now + timedelta(seconds=expires_in_seconds)).isoformat()
            with open('.env', 'w') as f:
                for line in lines:
                    if 'ACCESS_TOKEN' not in line and 'EXPIRES_IN' not in line:
                        f.write(line)
                    elif 'ACCESS_TOKEN' in line:
                        f.write(f"ACCESS_TOKEN={access_token}\n")
                        self.access_token = access_token
                    elif 'EXPIRES_IN' in line:
                        f.write(f"EXPIRES_IN={EXPIRATION_TIME}")
            return self.access_token
        return self.access_token
