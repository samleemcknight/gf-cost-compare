from unittest.mock import patch, MagicMock
from tests.test_data.products import mock_products
from tests.test_data.locations import mock_locations
from tests.test_data.chains import mock_chains


class MockData:

    locations = mock_locations
    products = mock_products
    chains = mock_chains

    def mock_data(self):
        locations_service_mock = MagicMock(name="LocationsServiceMock")

        def patch_get_locations(location_list):
            """
            patches get_locations() method in LocationsService
            """
            def locations_func(*args, **kwargs):
                return location_list

            locations_service_mock.return_value.get_locations_data = MagicMock(side_effect=locations_func)
            return locations_service_mock.return_value.get_locations_data

        locations_patcher = patch('grocery_api_client.services.locations_service.LocationsService.get_locations_data',
                                  patch_get_locations(self.locations))
        locations_patcher.start()

        def patch_get_location_details(location_list):
            """
            patches get_location_details() method in LocationsService
            """
            def locations_func(*args, **kwargs):
                location_id = kwargs['location_id'] if kwargs else args[0]
                location = [location for location in location_list if location['locationId'] == location_id]
                return location[0] if location else {}

            locations_service_mock.return_value.get_location_details_data = MagicMock(side_effect=locations_func)
            return locations_service_mock.return_value.get_location_details_data

        locations_patcher = patch(
            'grocery_api_client.services.locations_service.LocationsService.get_location_details_data',
            patch_get_location_details(self.locations)
        )
        locations_patcher.start()

        def patch_does_location_exist(location_list):
            """
            patches does_location_exist() method in LocationsService
            """
            def locations_func(*args, **kwargs):
                location_id = kwargs['location_id'] if kwargs else args[0]
                location = [location for location in location_list if location['locationId'] == location_id]
                return True if location else False

            locations_service_mock.return_value.does_location_exist = MagicMock(side_effect=locations_func)
            return locations_service_mock.return_value.does_location_exist

        locations_patcher = patch(
            'grocery_api_client.services.locations_service.LocationsService.does_location_exist',
            patch_does_location_exist(self.locations)
        )
        locations_patcher.start()

        def patch_get_chains(chains_list):
            """
            patches get_chains() method in LocationsService
            """
            def locations_func():
                return chains_list

            locations_service_mock.return_value.get_chains_data = MagicMock(side_effect=locations_func)
            return locations_service_mock.return_value.get_chains_data

        locations_patcher = patch(
            'grocery_api_client.services.locations_service.LocationsService.get_chains_data',
            patch_get_chains(self.chains)
        )
        locations_patcher.start()

        # products methods
        products_service_mock = MagicMock(name="ProductsServiceMock")

        def patch_get_products_from_location(products_list):
            def products_func(**kwargs):
                if len(products_list) > kwargs['product_limit']:
                    return products_list[0:kwargs['product_limit']]
                return products_list

            products_service_mock.return_value.get_products_data_from_location = \
                MagicMock(side_effect=products_func)
            return products_service_mock.return_value.get_products_data_from_location

        products_patcher = patch(
            'grocery_api_client.services.products_service.ProductsService.get_products_data_from_location',
            patch_get_products_from_location(self.products)
        )
        products_patcher.start()
