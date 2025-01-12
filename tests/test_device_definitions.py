import pytest
from unittest.mock import AsyncMock, MagicMock
from dimo.api.device_definitions import DeviceDefinitions


@pytest.fixture
def mock_request_method():
    """Fixture to mock the request method."""
    return AsyncMock()


@pytest.fixture
def mock_get_auth_headers():
    """Fixture to mock the header function."""
    return MagicMock(return_value={"Authorization": "Bearer test_token"})


@pytest.fixture
def device_definitions(mock_request_method, mock_get_auth_headers):
    """Fixture to provide a DeviceDefinitions object."""
    return DeviceDefinitions(mock_request_method, mock_get_auth_headers)


@pytest.mark.asyncio
async def test_decode_vin(
    device_definitions, mock_request_method, mock_get_auth_headers
):
    """Test the method decode_vin."""
    # Mock parameters
    developer_jwt = "test_jwt"
    country_code = "US"
    vin = "1HGCM82633A123456"

    # Mock the response from the request
    mock_response = {"decodedVin": {"make": "Honda", "model": "Accord", "year": 2003}}
    mock_request_method.return_value = mock_response

    # Call the method
    response = await device_definitions.decode_vin(developer_jwt, country_code, vin)

    # Assertions
    mock_request_method.assert_called_once_with(
        "POST",
        "DeviceDefinitions",
        "/device-definitions/decode-vin",
        headers={
            "Authorization": "Bearer test_token",
            "Content-Type": "application/json",
        },
        data={"countryCode": country_code, "vin": vin},
    )
    mock_get_auth_headers.assert_called_once_with(developer_jwt)
    assert response == mock_response


@pytest.mark.asyncio
async def test_search_device_definitions(device_definitions, mock_request_method):
    """Test the method search_device_definitions."""
    # Mock parameters
    query = "Honda Accord"
    make_slug = "honda"
    model_slug = "accord"
    year = 2003
    page = 1
    page_size = 10

    # Mock the response from the request
    mock_response = {
        "results": [
            {"make": "Honda", "model": "Accord", "year": 2003},
        ],
        "total": 1,
    }
    mock_request_method.return_value = mock_response

    # Call the method
    response = await device_definitions.search_device_definitions(
        query=query,
        make_slug=make_slug,
        model_slug=model_slug,
        year=year,
        page=page,
        page_size=page_size,
    )

    # Assertions
    mock_request_method.assert_called_once_with(
        "GET",
        "DeviceDefinitions",
        "/device-definitions/search",
        params={
            "query": query,
            "makeSlug": make_slug,
            "modelSlug": model_slug,
            "year": year,
            "page": page,
            "pageSize": page_size,
        },
    )
    assert response == mock_response
