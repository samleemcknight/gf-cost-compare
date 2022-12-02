from unittest.mock import patch, MagicMock
from tests.test_data.products import mock_products
from tests.test_data.locations import mock_locations

class MockData:

    locations = mock_locations
    products = mock_products

    def mock_product_controller(self):
        products_service_mock = MagicMock(name="ProductsServiceMock")

        def patch_get_locations(location_list):
            def locations_func(*args, **kwargs):
                return location_list

            products_service_mock.return_value.get_locations = MagicMock(side_effect=locations_func)

            return products_service_mock.return_value.get_locations

        locations_patcher = patch('grocery_api_client.services.locations_service.LocationsService.get_locations',
                                  patch_get_locations(self.locations))
        locations_patcher.start()

        def patch_get_products_from_location(products_list):
            def products_func(*args, **kwargs):
                if len(products_list) > kwargs['product_limit']:
                    return products_list[0:kwargs['product_limit']]
                return products_list

            products_service_mock.return_value.get_products_from_location = \
                MagicMock(side_effect=products_func)
            return products_service_mock.return_value.get_products_from_location

        products_patcher = patch(
            'grocery_api_client.services.products_service.ProductsService.get_products_from_location',
            patch_get_products_from_location(self.products)
        )
        products_patcher.start()
