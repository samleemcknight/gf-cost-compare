import pytest
from mock import patch

from product_controller import ProductController
from tests.mock_modules import MockData


@pytest.fixture
@patch('authenticate.Authenticate')
def mock_authenticate(mock_authenticate):
    return mock_authenticate


@pytest.fixture
def mock_product_control_data():
    return MockData().mock_product_controller()


@pytest.fixture
def product_controller(mock_authenticate):
    return ProductController(mock_authenticate)
