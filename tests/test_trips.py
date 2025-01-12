import pytest
from unittest.mock import AsyncMock
from dimo.errors import DimoTypeError
from dimo.api.trips import Trips


@pytest.fixture
def mock_request_method():
    return AsyncMock()


@pytest.fixture
def mock_get_auth_headers():
    return lambda jwt: {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json",
    }


@pytest.fixture
def trips_instance(mock_request_method, mock_get_auth_headers):
    return Trips(
        request_method=mock_request_method, get_auth_headers=mock_get_auth_headers
    )


@pytest.mark.asyncio
async def test_trips_happy_path(trips_instance, mock_request_method):
    vehicle_jwt = "valid_jwt"
    token_id = 123
    page = 5

    expected_url = "/v1/vehicle/123/trips"
    expected_headers = {
        "Authorization": "Bearer valid_jwt",
        "Content-Type": "application/json",
    }
    expected_params = {"page": [page]}

    mock_request_method.return_value = {"data": "mock_response"}

    response = await trips_instance.trips(vehicle_jwt, token_id, page)

    mock_request_method.assert_awaited_once_with(
        "GET",
        "Trips",
        expected_url,
        params=expected_params,
        headers=expected_headers,
    )
    assert response == {"data": "mock_response"}


@pytest.mark.asyncio
async def test_trips_no_page_param(trips_instance, mock_request_method):
    vehicle_jwt = "valid_jwt"
    token_id = 456

    expected_url = "/v1/vehicle/456/trips"
    expected_headers = {
        "Authorization": "Bearer valid_jwt",
        "Content-Type": "application/json",
    }
    expected_params = {}

    mock_request_method.return_value = {"data": "mock_response_no_page"}

    response = await trips_instance.trips(vehicle_jwt, token_id)

    mock_request_method.assert_awaited_once_with(
        "GET",
        "Trips",
        expected_url,
        params=expected_params,
        headers=expected_headers,
    )
    assert response == {"data": "mock_response_no_page"}


@pytest.mark.parametrize(
    "vehicle_jwt, token_id, expected_error",
    [
        (123, 456, DimoTypeError),  # vehicle_jwt kein String
        ("valid_jwt", "abc", DimoTypeError),  # token_id keine Zahl
    ],
)
@pytest.mark.asyncio
async def test_trips_invalid_params(
    vehicle_jwt, token_id, expected_error, trips_instance
):
    with pytest.raises(expected_error):
        await trips_instance.trips(vehicle_jwt, token_id)
