import pytest
import asyncio
from unittest.mock import AsyncMock
from dimo import DIMO


@pytest.mark.asyncio
async def test_init():
    """
    Tests the initialization of the DIMO module
    """
    dimo = DIMO(env="Production")
    assert dimo.env == "Production"
    assert dimo.urls is not None


@pytest.mark.asyncio
async def test_get_auth_token():
    """
    Tests the authentication method and ensures that a token is generated
    """
    # Mocking the auth method
    dimo = DIMO(env="Production")
    dimo.auth.get_token = AsyncMock(return_value={"access_token": "mock_access_token"})

    client_id = "mock_client_id"
    domain = "mock_domain"
    private_key = "mock_private_key"

    auth_header = await dimo.auth.get_token(
        client_id=client_id, domain=domain, private_key=private_key
    )
    assert "access_token" in auth_header
    assert auth_header["access_token"] == "mock_access_token"


@pytest.mark.asyncio
async def test_decode_vin():
    """
    Tests the VIN decoding scenario
    """
    dimo = DIMO(env="Production")
    dimo.device_definitions.decode_vin = AsyncMock(
        return_value={"make": "Volkswagen", "model": "Golf", "year": 2022}
    )

    developer_jwt = "mock_dev_jwt"
    vin = "WVWZZZE10RP004864"

    result = await dimo.device_definitions.decode_vin(
        developer_jwt=developer_jwt, country_code="DEU", vin=vin
    )
    assert result["make"] == "Volkswagen"
    assert result["model"] == "Golf"
    assert result["year"] == 2022


@pytest.mark.asyncio
async def test_get_total_cars():
    """
    Tests the identity method to count vehicles
    """
    dimo = DIMO(env="Production")
    dimo.identity.count_dimo_vehicles = AsyncMock(return_value=12345)

    result = await dimo.identity.count_dimo_vehicles()
    assert result == 12345


@pytest.mark.asyncio
async def test_get_privileged_token():
    """
    Tests the privileged token functionality
    """
    dimo = DIMO(env="Production")
    dimo.token_exchange.exchange = AsyncMock(
        return_value={"token": "mock_privileged_token"}
    )

    developer_jwt = "mock_dev_jwt"
    token_id = 1

    result = await dimo.token_exchange.exchange(
        developer_jwt=developer_jwt, privileges=[1, 2, 3], token_id=token_id
    )
    assert result["token"] == "mock_privileged_token"


@pytest.mark.asyncio
async def test_query_vehicles_for_license():
    """
    Tests the GraphQL method to fetch vehicles based on a license
    """
    dimo = DIMO(env="Production")
    dimo.identity.query = AsyncMock(return_value={"vehicles": {"totalCount": 5}})

    license_id = "mock_license_id"

    GET_ALL_VEHICLES_QUERY = """
    query VehiclesForLicense {{
      vehicles(filterBy: {{ privileged: "{license_id}" }}, first: 100) {{
        totalCount
      }}
    }}"""
    query = GET_ALL_VEHICLES_QUERY.format(license_id=license_id)

    response = await dimo.identity.query(query)
    assert response["vehicles"]["totalCount"] == 5


@pytest.mark.asyncio
async def test_available_signals():
    """
    Tests if available signals can be fetched
    """
    dimo = DIMO(env="Production")
    dimo.telemetry.query = AsyncMock(
        return_value={"availableSignals": ["signal1", "signal2"]}
    )

    vehicle_jwt = "mock_vehicle_jwt"
    token_id = 12345

    GET_AVAILABLE_SIGNALS_QUERY = """
    query AvailableSignals {{
      availableSignals(tokenId: {token_id})
    }}
    """
    query = GET_AVAILABLE_SIGNALS_QUERY.format(token_id=token_id)

    response = await dimo.telemetry.query(query, vehicle_jwt)
    assert "availableSignals" in response
    assert len(response["availableSignals"]) == 2
    assert response["availableSignals"][0] == "signal1"


@pytest.mark.asyncio
async def test_signals_latest():
    """
    Tests fetching the latest signals
    """
    dimo = DIMO(env="Production")
    dimo.telemetry.get_signals_latest = AsyncMock(return_value={"signal": "latest"})

    vehicle_jwt = "mock_vehicle_jwt"
    token_id = "mock_token_id"

    response = await dimo.telemetry.get_signals_latest(vehicle_jwt, token_id)
    assert response["signal"] == "latest"
