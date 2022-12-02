import pytest
from mock import patch

from grocery_api_client.services.products_service import ProductsService
from tests.mock_modules import MockData


@pytest.fixture
@patch('grocery_api_client.services.authentication_service.AuthenticationService')
def mock_authentication_service(mock_authentication_service):
    return mock_authentication_service


@pytest.fixture
def mock_product_control_data():
    return MockData().mock_product_controller()


@pytest.fixture
def products_service(mock_authentication_service):
    return ProductsService(mock_authentication_service)
