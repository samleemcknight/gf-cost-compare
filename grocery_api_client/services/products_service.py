from typing import List
from dotenv import load_dotenv
import requests
import json
from grocery_api_client.services.helpers.constants import KROGER_PRODUCTS_URI
from grocery_api_client.services.locations_service import LocationsService
from models import Product


class ProductsService:
    """
    Service for getting products from Kroger API
    """
    load_dotenv()

    def __init__(self,
                 access_token: str,
                 search_radius_miles: int = 10):
        self.access_token = access_token
        self.product_uri = KROGER_PRODUCTS_URI
        self.locations_service = LocationsService(self.access_token, search_radius_miles)

    def get_products_from_location(self,
                                   filter_term: str,
                                   location_id: str,
                                   product_limit: int):
        """
        :param filter_term: all lower case, no spaces string name of product
        :param location_id: ID of store
        :param product_limit: max number of products returned
        :return: dictionary of products directly from Kroger Products API
        """
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
                                                      product_limit: int = 50) -> Product:
        """
        Custom method for determining the minimum priced product given a location.
        If there are no products returned, that means that either the Kroger affiliates near you
        do not carry the specific product, there is a type in the name, or you need to expand `search_radius_miles`
        when you instantiate ProductsService
        :param product_name: all lower case, no spaces name of product
        :param zip_code: 5-digit US zip code
        :param product_limit: max number of products returned in one request
        :return: single Product object. (empty object if no products have been found)
        """
        product_info = self.get_product_list(product_name=product_name,
                                             zip_code=zip_code,
                                             product_limit=product_limit)
        if not product_info:
            return Product()
        large = small = product_info[0].price
        min_index = 0
        for index, product in enumerate(product_info):
            if product.price > large:
                large = product.price
            if product.price < small:
                small = product.price
                min_index = index
        return product_info[min_index]

    def get_product_list(self,
                         product_name: str,
                         zip_code: int,
                         product_limit: int = 50) -> List[Product]:
        """
        :param product_name: all lower case, no spaces name of product
        :param zip_code: 5-digit US zip code
        :param product_limit: max number of products returned in one request
        :return: list of Product objects
        """
        locations = self.locations_service.get_locations(zip_code)
        location_id = locations[0]['locationId']
        products = self.get_products_from_location(filter_term=product_name,
                                                   location_id=location_id,
                                                   product_limit=product_limit)
        if not products:
            return []

        product_info = self.create_product_objects_from_api_response(products)
        return product_info

    @staticmethod
    def create_product_objects_from_api_response(product_data: List[dict]) -> List[Product]:
        product_info = []
        for product_dict in product_data:
            if len(product_dict['items']) == 1:
                product = Product(product_id=product_dict['productId'],
                                  description=product_dict['description'],
                                  price=product_dict['items'][0]['price']['regular'],
                                  size_string=product_dict['items'][0]['size'])
                product_info.append(product)
        return product_info
