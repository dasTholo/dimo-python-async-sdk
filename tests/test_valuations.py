import pytest
from unittest.mock import AsyncMock
from dimo.errors import DimoTypeError
from dimo.api.valuations import Valuations


@pytest.fixture
def mock_request_method():
    """
    Fixture, das eine Mock-Implementierung für den asynchronen Request liefert.
    """
    return AsyncMock()


@pytest.fixture
def mock_get_auth_headers():
    """
    Fixture, das Header-Daten simuliert.
    """
    return lambda jwt: {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json",
    }


@pytest.fixture
def valuations_instance(mock_request_method, mock_get_auth_headers):
    """
    Fixture, das eine Instanz der `Valuations`-Klasse mit gemockten Abhängigkeiten zurückgibt.
    """
    return Valuations(
        request_method=mock_request_method, get_auth_headers=mock_get_auth_headers
    )


@pytest.mark.asyncio
async def test_get_valuations_happy_path(valuations_instance, mock_request_method):
    """
    Testet die Methode `get_valuations` mit korrekten Eingaben.
    """
    # Arrange
    vehicle_jwt = "valid_jwt"
    token_id = 789
    expected_url = "/v2/vehicles/789/valuations"
    expected_headers = {
        "Authorization": "Bearer valid_jwt",
        "Content-Type": "application/json",
    }
    mock_request_method.return_value = {"data": "mock_valuations_data"}

    # Act
    response = await valuations_instance.get_valuations(vehicle_jwt, token_id)

    # Assert
    mock_request_method.assert_awaited_once_with(
        "GET", "Valuations", expected_url, headers=expected_headers
    )
    assert response == {"data": "mock_valuations_data"}


@pytest.mark.asyncio
async def test_offers_lookup_happy_path(valuations_instance, mock_request_method):
    """
    Testet die Methode `offers_lookup` mit korrekten Eingaben.
    """
    # Arrange
    vehicle_jwt = "valid_jwt"
    token_id = 456
    expected_url = "v2/vehicles/456/instant-offer"
    expected_headers = {
        "Authorization": "Bearer valid_jwt",
        "Content-Type": "application/json",
    }
    mock_request_method.return_value = None

    # Act
    response = await valuations_instance.offers_lookup(vehicle_jwt, token_id)

    # Assert
    mock_request_method.assert_awaited_once_with(
        "GET", "Valuations", expected_url, headers=expected_headers
    )
    assert response is None


@pytest.mark.asyncio
async def test_list_vehicle_offers_happy_path(valuations_instance, mock_request_method):
    """
    Testet die Methode `list_vehicle_offers` mit korrekten Eingaben.
    """
    # Arrange
    vehicle_jwt = "valid_jwt"
    token_id = 101
    expected_url = "/v2/vehicles/101/offers"
    expected_headers = {
        "Authorization": "Bearer valid_jwt",
        "Content-Type": "application/json",
    }
    mock_request_method.return_value = {"offers": ["offer1", "offer2"]}

    # Act
    response = await valuations_instance.list_vehicle_offers(vehicle_jwt, token_id)

    # Assert
    mock_request_method.assert_awaited_once_with(
        "GET", "Valuations", expected_url, headers=expected_headers
    )
    assert response == {"offers": ["offer1", "offer2"]}


@pytest.mark.parametrize(
    "vehicle_jwt, token_id, expected_error",
    [
        (123, 456, DimoTypeError),  # vehicle_jwt kein String
        ("valid_jwt", "abc", DimoTypeError),  # token_id keine Zahl
    ],
)
@pytest.mark.asyncio
async def test_invalid_params(
    vehicle_jwt, token_id, expected_error, valuations_instance
):
    """
    Testet ungültige Eingabeparameter, die Typfehler auslösen sollen.
    """
    with pytest.raises(expected_error):
        await valuations_instance.get_valuations(vehicle_jwt, token_id)

    with pytest.raises(expected_error):
        await valuations_instance.offers_lookup(vehicle_jwt, token_id)

    with pytest.raises(expected_error):
        await valuations_instance.list_vehicle_offers(vehicle_jwt, token_id)
