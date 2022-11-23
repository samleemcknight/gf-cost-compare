import logging
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests
import base64
import json

load_dotenv()

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
AUTH_TOKEN = f"{CLIENT_ID}:{CLIENT_SECRET}".encode("ascii")
PRODUCTION_URI = os.environ.get('PRODUCTION_URI')
OAUTH_CONNECT_URI = os.environ.get('OAUTH_CONNECT_URI')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
SCOPE = 'product.compact'
encoded_token = base64.b64encode(AUTH_TOKEN)
encoded_string = encoded_token.decode('ascii')

now = datetime.utcnow()

with open('.env', 'r') as f:
    lines = f.readlines()

old_expires_in = [line for line in lines if 'EXPIRES_IN' in line]
old_expiration_time_string = datetime.fromisoformat(old_expires_in[0].split('=')[1].replace('\n', ''))

if now >= old_expiration_time_string:
    auth_resp = requests.post(OAUTH_CONNECT_URI,
                              headers={
                                  "Authorization": f"Basic {encoded_string}",
                                  "Content-Type": "application/x-www-form-urlencoded"
                              },
                              data={
                                  "grant_type": "client_credentials",
                                  "scope": SCOPE
                              })

    assert auth_resp.status_code == 200
    auth_response = json.loads(auth_resp.content)
    auth_token = auth_response['access_token']
    expires_in_seconds = auth_response['expires_in']
    EXPIRATION_TIME = (now + timedelta(seconds=expires_in_seconds)).isoformat()
    with open('.env', 'w') as f:
        for line in lines:
            if 'ACCESS_TOKEN' not in line and 'EXPIRES_IN' not in line:
                f.write(f"{line}\n")
            elif 'ACCESS_TOKEN' in line:
                f.write(f"ACCESS_TOKEN={auth_token}\n")
            elif 'EXPIRES_IN' in line:
                f.write(f"EXPIRES_IN={EXPIRATION_TIME}\n")

logging.info('authentication successful')
