import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from dimo.api.token_exchange import TokenExchange


@pytest.fixture
def mock_request_method():
    """Fixture zum Mocken der Anfrage-Methode."""
    return AsyncMock()


@pytest.fixture
def mock_get_auth_headers():
    """Fixture zum Mocken der Header-Funktion."""
    return MagicMock(return_value={"Authorization": "Bearer test_token"})


@pytest.fixture
def token_exchange(mock_request_method, mock_get_auth_headers):
    """Fixture, um ein TokenExchange-Objekt bereitzustellen."""
    return TokenExchange(mock_request_method, mock_get_auth_headers)


@pytest.mark.asyncio
@patch("dimo.api.token_exchange.dimo_constants", {"Production": {"NFT_address": "0x123456789abcdef"}})
async def test_exchange(token_exchange, mock_request_method, mock_get_auth_headers):
    """Test der Methode exchange."""
    # Mock-Parameter
    developer_jwt = "test_jwt"
    privileges = ["view_data"]
    token_id = 12345
    env = "Production"

    # Mock der Antwort vom Request
    mock_response = {"success": True, "newToken": "newMockedToken"}
    mock_request_method.return_value = mock_response

    # Methode aufrufen
    response = await token_exchange.exchange(
        developer_jwt=developer_jwt, privileges=privileges, token_id=token_id, env=env
    )

    # Assertions
    mock_request_method.assert_called_once_with(
        "POST",
        "TokenExchange",
        "/v1/tokens/exchange",
        headers={"Authorization": "Bearer test_token"},
        data={
            "nftContractAddress": "0x123456789abcdef",
            "privileges": privileges,
            "tokenId": token_id,
        },
    )
    mock_get_auth_headers.assert_called_once_with(developer_jwt)
    assert response == mock_response
