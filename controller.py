import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

PRODUCTION_URI = os.environ.get('PRODUCTION_URI')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

product_url = f"{PRODUCTION_URI}?filter.term=bread.filter.limit=50"

resp = requests.get(product_url, headers={
    "Accept": "application/json",
    "Authorization": f"Bearer {ACCESS_TOKEN}"
})

assert resp.status_code == 200
products = json.loads(resp.content)

assert products
