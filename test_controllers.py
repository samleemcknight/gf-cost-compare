import json
from product_controller import ProductController

# grocery_file = open('./data.json')
#
# data = json.load(grocery_file)
#
# products = {'items': {}}
# for item in data[0]['data']['products']:
#     item_id = int(item['id'])
#     item_name = item['item'].get('description', 'N/A')
#     item_price = item['price']['storePrices']['regular']['price'] if item.get('price') else 'N/A'
#     products['items'].update({item_id: {'name': item_name, 'price': item_price}})
#
# prices = []
# for key, value in products['items'].items():
#     price = float(value['price'].split('USD ')[1]) if value['price'] != 'N/A' else 0
#     if price:
#         prices.append(price)
#
# i = 0
#
# print(min(prices))

controller = ProductController(search_radius_miles=5)

product = controller.determine_minimum_priced_product_for_location(product_name='oats',
                                                                   zip_code=80123)

print(product)

product_list = controller.get_product_list(product_name='oats',
                                           zip_code=80123,
                                           product_limit=25)
print('\n\n')
print(product_list)
