import json
import requests

grocery_file = open('./data.json')

data = json.load(grocery_file)

products = {'items': {}}
for item in data[0]['data']['products']:
    item_id = int(item['id'])
    item_name = item['item'].get('description', 'N/A')
    item_price = item['price']['storePrices']['regular']['price'] if item.get('price') else 'N/A'
    products['items'].update({item_id: {'name': item_name, 'price': item_price}})

prices = []
for key, value in products['items'].items():
    price = float(value['price'].split('USD ')[1]) if value['price'] != 'N/A' else 0
    if price:
        prices.append(price)

i = 0

print(min(prices))
