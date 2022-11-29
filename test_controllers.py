from product_controller import ProductController

controller = ProductController(search_radius_miles=5)

product = controller.determine_minimum_priced_product_for_location(product_name='frozenpizza',
                                                                   zip_code=80123)

print(product.__dict__)
print(product.price_per_unit())

product_list = controller.get_product_list(product_name='oats',
                                           zip_code=80123,
                                           product_limit=25)
print('\n\n')
print(product_list)
