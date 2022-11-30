from product_controller import ProductController

controller = ProductController(search_radius_miles=5)

product = controller.determine_minimum_priced_product_for_location(product_name='frozenpizza',
                                                                   zip_code=80123)

assert product.product_id
assert product.price
assert product.size()

product_list = controller.get_product_list(product_name='milk',
                                           zip_code=80123,
                                           product_limit=10)
# assert len(product_list)
print([product.__dict__ for product in product_list])
