from models import Product


def test_get_access_key(mock_authentication_service):
    token = mock_authentication_service.get_auth_access_token()
    assert token


def test_get_locations(mock_product_control_data,
                       locations_service,
                       products_service,
                       mock_authentication_service):
    locations = locations_service.get_locations(zip_code=80123)
    assert len(locations)
    assert locations[0]['chain'] == 'KROGER'


def test_get_products_from_location(mock_product_control_data,
                                    products_service):
    locations = products_service.locations_service.get_locations(zip_code=80123)
    products = products_service.get_products_from_location(filter_term='milk',
                                                           location_id=locations[0]['locationId'],
                                                           product_limit=10)
    assert len(products) <= 10


def test_determine_minimum_priced_product_for_location(mock_product_control_data,
                                                       products_service):
    min_priced_product = products_service.determine_minimum_priced_product_for_location(
        product_name='pasta',
        zip_code=12345,
        product_limit=10)

    assert isinstance(min_priced_product, Product)


def test_get_product_list(mock_product_control_data,
                          products_service):
    products = products_service.get_product_list(product_name='oats',
                                                 zip_code=12312,
                                                 product_limit=5)
    assert len(products) == 5
