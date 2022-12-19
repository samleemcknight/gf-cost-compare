import pytest
from mock import patch

from grocery_api_client import ProductsService
from grocery_api_client import LocationsService
from tests.mock_modules import MockData


@pytest.fixture
@patch('grocery_api_client.services.authentication_service.AuthenticationService')
def mock_authentication_service(mock_authentication_service):
    return mock_authentication_service


@pytest.fixture
def mock_access_token(mock_authentication_service):
    return mock_authentication_service.get_auth_access_token()


@pytest.fixture
def mock_data():
    return MockData().mock_data()


@pytest.fixture
def products_service(mock_access_token):
    return ProductsService(mock_access_token)


@pytest.fixture
def locations_service(mock_access_token):
    return LocationsService(mock_access_token)
