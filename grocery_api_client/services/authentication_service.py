import base64
import json
import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from requests import Response
from grocery_api_client.services.helpers.constants import KROGER_OAUTH_URI


class AuthenticationService:
    """
    Service for authenticating to Kroger API. In order to work, you must have the following
    valid Kroger client_id and client_secret set as API environment variables e.g.:
    CLIENT_ID=abc1234la851
    CLIENT_SECRET=09slae423gk5ace6yui
    """
    load_dotenv()

    def __init__(self,
                 scope: str = 'product.compact'):
        self.client_id = os.environ.get('CLIENT_ID')
        self.client_secret = os.environ.get('CLIENT_SECRET')
        self.auth_token = f"{self.client_id}:{self.client_secret}".encode("ascii")
        self.oauth_connect_uri = KROGER_OAUTH_URI
        self.access_token = os.environ.get('ACCESS_TOKEN')
        self.expires_in = os.environ.get('EXPIRES_IN')
        self.scope = scope

    def get_auth_access_token(self,
                              write_to_env_file: bool = False) -> str:
        """
        :param write_to_env_file: for local development, if True will save non-expired access token to .env file
        :return: string access token for accessing kroger location and product APIs

        The access token will last for 30 minutes, however unless you set `write_to_env_file` to `True`, the method
        will continue making calls to Kroger's OAuth client. In order to reduce the number of calls, add
        ACCESS_TOKEN and EXPIRES_IN to your `.env` file (no values necessary - those will be written for you)
        """
        if write_to_env_file and self.__token_is_not_expired():
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
        """
        :return: OAuth response
        """
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

    def __token_is_not_expired(self) -> bool:
        """
        This method simply checks to see whether the expires_in ISO string is greater than
        datetime.utcnow()
        Note: the validation will return True if you adjust your expires_in time to the future,
        but your API calls will return 403s.
        :return:
        """
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
        with open(file='.env', mode='r', encoding="utf-8") as f:
            lines = f.readlines()
        with open(file='.env', mode='w', encoding="utf-8") as f:
            for line in lines:
                if 'ACCESS_TOKEN' not in line and 'EXPIRES_IN' not in line:
                    f.write(line)
                elif 'ACCESS_TOKEN' in line:
                    f.write(f"ACCESS_TOKEN={access_token}\n")
                    self.access_token = access_token
                elif 'EXPIRES_IN' in line:
                    f.write(f"EXPIRES_IN={expiration_time}")
