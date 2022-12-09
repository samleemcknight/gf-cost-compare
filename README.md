# gf-cost-compare

## Overview
Millions of people in the USA suffer from celiac disease or other medically diagnosed gluten intolerances 
and have to pay on average hundreds of dollars more for groceries each year than people without these food requirements. 
The US tax code allows writing off gluten-free food that is "in excess of the cost of the gluten containing food 
that you are replacing", however this is a difficult task since people with these conditions are not replacing any 
food, but simply buying their groceries. This process would benefit from a streamlined way to find comparable 
non gluten-free items and show the amount one may write off for the gluten-free item.

## Kroger API
This is a client that interacts with the Kroger Location and Product APIs and returns relevant data given a 
zip code and generic name e.g. 'bread', 'pasta', 'flour', 'oats', etc. The relevant data can include the minimum priced
product, a list of products, or the product price per weight.

### Example implementation:

```python
from grocery_api_client import AuthenticationService, LocationsService, ProductsService
from grocery_api_client.models import Product

search_radius = 25
zip_code = 90210
product_name = 'bread'
product_limit = 100

# note that this token will only be good for 30 minutes at a time
access_token  = AuthenticationService().get_auth_access_token()

products_service = ProductsService(access_token=access_token,
                                   search_radius_miles=search_radius)

locations_service = LocationsService(access_token=access_token,
                                     search_radius_miles=search_radius)

# Get minimum priced product
product: Product = products_service.determine_minimum_priced_product_for_location(product_name=product_name,
                                                                                  zip_code=zip_code,
                                                                                  product_limit=product_limit)

# Get list of products
products: [Product] = products_service.get_product_list(product_name=product_name,
                                                        zip_code=zip_code,
                                                        product_limit=product_limit)

# Get list of locations near you
locations: [dict] = locations_service.get_locations(zip_code=zip_code)

# Get list of products from location. This returns the raw data from the Kroger API 
products: [dict] = products_service.get_products_from_location(filter_term=product_name,
                                                               location_id=locations[0]['locationId'],
                                                               product_limit=product_limit)
```
_Note: the API by default will return any location near you even if that is a gas station or deli_
