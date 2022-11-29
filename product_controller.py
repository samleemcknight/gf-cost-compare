import os
from typing import List
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
        if not locations:
            raise Exception(f'No locations were found for your area. Please select a wider '
                            f'search radius than {self.search_radius_miles} miles')
        return locations['data']

    def get_products_from_location(self,
                                   filter_term: str,
                                   location_id: str,
                                   product_limit: int):
        product_url = f"{self.product_uri}?filter.term={filter_term}&" \
                      f"filter.locationId={location_id}&filter.limit={product_limit}"
        resp = requests.get(product_url, headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        })

        products = json.loads(resp.content)

        return products['data']

    def determine_minimum_priced_product_for_location(self,
                                                      product_name: str,
                                                      zip_code: int,
                                                      product_limit: int = 50) -> dict:
        product_info = self.get_product_list(product_name=product_name,
                                             zip_code=zip_code,
                                             product_limit=product_limit)
        if not product_info:
            return {}
        large = small = product_info[0]['price']
        min_index = 0
        for index, price in enumerate(product_info):
            if price['price'] > large:
                large = price['price']
            if price['price'] < small:
                small = price['price']
                min_index = index
        return product_info[min_index]

    def get_product_list(self,
                         product_name: str,
                         zip_code: int,
                         product_limit: int = 50) -> List[dict]:
        locations = self.get_locations(zip_code)
        location_id = locations[0]['locationId']
        products = self.get_products_from_location(filter_term=product_name,
                                                   location_id=location_id,
                                                   product_limit=product_limit)
        if not products:
            return []

        product_info = self.get_relevant_product_data(products)
        return product_info

    @staticmethod
    def get_relevant_product_data(products: List[dict]):
        product_info = []
        for product in products:
            if len(product['items']) == 1:
                product_info.append({
                    'product_id': product['productId'],
                    'description': product['description'],
                    'price': product['items'][0]['price']['regular'],
                    'size': product['items'][0]['size']
                })
        return product_info
