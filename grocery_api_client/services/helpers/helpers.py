from typing import List
from grocery_api_client.models import Product, Location


def create_product_objects_from_api_response(product_data: List[dict]) -> List[Product]:
    products = []
    for product_dict in product_data:
        if len(product_dict['items']) == 1:
            product = Product(product_id=product_dict['productId'],
                              description=product_dict['description'],
                              price=product_dict['items'][0]['price']['regular'],
                              size_string=product_dict['items'][0]['size'])
            products.append(product)
    return products


def create_location_objects_from_api_response(location_data: List[dict]) -> List[Location]:
    locations = []
    for location_dict in location_data:
        location = Location(location_id=location_dict['locationId'],
                            name=location_dict['name'],
                            chain=location_dict['chain'],
                            departments=location_dict.get('departments', []),
                            address=location_dict['address'])
        locations.append(location)
    return locations


def return_or_raise(return_object,
                    exception,
                    exception_message: str = None):
    if return_object:
        return return_object
    raise exception(exception_message)
