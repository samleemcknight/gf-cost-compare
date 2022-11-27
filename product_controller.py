import os
from dotenv import load_dotenv
import requests
import json
from authenticate import Authenticate


class ProductController:

    load_dotenv()

    def __init__(self,
                 search_radius_miles: int = 10):
        self.authentication = Authenticate()
        self.access_token = self.authentication.get_auth_access_token()
        self.product_uri = os.environ.get('PRODUCT_URI')
        self.location_uri = os.environ.get('LOCATION_URI')
        self.search_radius_miles = search_radius_miles

    def get_locations(self,
                      zip_code: int):
        location_url = f"{self.location_uri}?filter.zipCode.near={zip_code}" \
                       f"&filter.radiusInMiles={self.search_radius_miles}"
        resp = requests.get(location_url, headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        })
        locations = json.loads(resp.content)
        return locations['data']

    def get_products(self,
                     zip_code: int,
                     filter_term: str):
        locations = self.get_locations(zip_code)
        if locations:
            location_id = locations[0]['locationId']
            product_url = f"{self.product_uri}?filter.term={filter_term}&" \
                          f"filter.locationId={location_id}&filter.limit=50"
        else:
            product_url = f"{self.product_uri}?filter.term={filter_term}&filter.limit=50"
        resp = requests.get(product_url, headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        })

        products = json.loads(resp.content)

        return products['data']

    def determine_minimum_priced_product(self,
                                         generic_product_name: str,
                                         zip_code: int):
        products = self.get_products(zip_code=zip_code,
                                     filter_term=generic_product_name)
        if not products:
            return []
        product_info = []
        for product in products:
            if len(product['items']) == 1:
                product_info.append({
                    'product_id': product['productId'],
                    'product_description': product['description'],
                    'product_price': product['items'][0]['price']['regular']
                })
        large = small = product_info[0]['product_price']
        min_index = 0
        for index, price in enumerate(product_info):
            if price['product_price'] > large:
                large = price['product_price']
            if price['product_price'] < small:
                small = price['product_price']
                min_index = index
        return product_info[min_index]

