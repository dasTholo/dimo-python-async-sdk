import pytest
from unittest.mock import AsyncMock
from dimo.api.attestation import Attestation
from dimo.errors import DimoTypeError  # Import der benutzerdefinierten Exception


@pytest.fixture
def mock_request():
    """Mocked request method fixture."""
    return AsyncMock()


@pytest.fixture
def mock_get_auth_headers():
    """Mocked get_auth_headers method fixture."""
    return lambda jwt: {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json",
    }


@pytest.fixture
def attestation(mock_request, mock_get_auth_headers):
    """Setup Attestation instance with mocked dependencies."""
    return Attestation(mock_request, mock_get_auth_headers)


@pytest.mark.asyncio
async def test_create_vin_vc_success(attestation, mock_request):
    """Test successful creation of VIN VC."""
    # Arrange
    vehicle_jwt = "valid_vehicle_jwt"
    token_id = 123
    expected_url = "/v1/vc/vin/123"
    expected_params = {"force": True}
    expected_headers = {
        "Authorization": f"Bearer {vehicle_jwt}",
        "Content-Type": "application/json",
    }

    mock_request.return_value = {"status": "success", "data": "dummy_data"}

    # Act
    response = await attestation.create_vin_vc(vehicle_jwt, token_id)

    # Assert
    mock_request.assert_called_once_with(
        "POST",
        "Attestation",
        expected_url,
        params=expected_params,
        headers=expected_headers,
    )
    assert response == {"status": "success", "data": "dummy_data"}


@pytest.mark.asyncio
async def test_create_pom_vc_success(attestation, mock_request):
    """Test successful creation of POM VC."""
    # Arrange
    vehicle_jwt = "valid_vehicle_jwt"
    token_id = 456
    expected_url = "/v1/vc/pom/456"
    expected_headers = {
        "Authorization": f"Bearer {vehicle_jwt}",
        "Content-Type": "application/json",
    }

    mock_request.return_value = {"status": "success", "data": "dummy_data"}

    # Act
    response = await attestation.create_pom_vc(vehicle_jwt, token_id)

    # Assert
    mock_request.assert_called_once_with(
        "POST",
        "Attestation",
        expected_url,
        headers=expected_headers,
    )
    assert response == {"status": "success", "data": "dummy_data"}


@pytest.mark.asyncio
async def test_create_vin_vc_invalid_token_id(attestation):
    """Test VIN VC creation with invalid token_id."""
    # Arrange
    vehicle_jwt = "valid_vehicle_jwt"
    token_id = "invalid_token_id"  # Should be int

    # Act & Assert
    with pytest.raises(DimoTypeError, match="token_id must be a int"):
        await attestation.create_vin_vc(vehicle_jwt, token_id)


@pytest.mark.asyncio
async def test_create_pom_vc_invalid_vehicle_jwt(attestation):
    """Test POM VC creation with invalid vehicle_jwt."""
    # Arrange
    vehicle_jwt = 12345  # Should be str
    token_id = 456

    # Act & Assert
    with pytest.raises(DimoTypeError, match="vehicle_jwt must be a str"):
        await attestation.create_pom_vc(vehicle_jwt, token_id)
