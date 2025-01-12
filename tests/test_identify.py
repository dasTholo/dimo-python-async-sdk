import pytest
from unittest.mock import AsyncMock

from dimo import DIMO
from dimo.graphql.identity import Identity


@pytest.fixture
def identity_instance():
    """
    Creates a mock instance of the Identity class for testing
    """
    dimo = DIMO(env="Production")
    dimo.query = AsyncMock()  # Mock the query method
    return Identity(dimo)


@pytest.mark.asyncio
async def test_count_dimo_vehicles(identity_instance):
    """
    Tests the count_dimo_vehicles method
    """
    # Define a mock response
    mock_response = {"vehicles": {"totalCount": 10}}
    identity_instance.dimo.query.return_value = mock_response

    result = await identity_instance.count_dimo_vehicles()

    assert result == mock_response
    identity_instance.dimo.query.assert_awaited_once_with(
        "Identity",
        """
      {
          vehicles (first:10) {
              totalCount,
          }
      }
      """,
    )


@pytest.mark.asyncio
async def test_list_vehicle_definitions_per_address(identity_instance):
    """
    Tests the list_vehicle_definitions_per_address method
    """
    # Define a mock response
    mock_response = {
        "vehicles": {
            "nodes": [
                {
                    "aftermarketDevice": {"tokenId": 1, "address": "mock_address_1"},
                    "definition": {"make": "Tesla", "model": "Model S", "year": 2022},
                }
            ]
        }
    }
    identity_instance.dimo.query.return_value = mock_response

    address = "0xMockAddress"
    limit = 5
    result = await identity_instance.list_vehicle_definitions_per_address(
        address, limit
    )

    assert result == mock_response
    identity_instance.dimo.query.assert_awaited_once_with(
        "Identity",
        """
      query ListVehicleDefinitionsPerAddress($owner: Address!, $first: Int!) {
        vehicles(filterBy: {owner: $owner}, first: $first) {
          nodes {
            aftermarketDevice {
              tokenId
              address
            } 
            syntheticDevice {
              address
              tokenId
            }
            definition {
              make
              model
              year
            }
          }
        }
      }
      """,
        variables={"owner": address, "first": limit},
    )


@pytest.mark.asyncio
async def test_mmy_by_owner(identity_instance):
    """
    Tests the mmy_by_owner method
    """
    # Define a mock response
    mock_response = {
        "vehicles": {
            "nodes": [
                {"definition": {"make": "Tesla", "model": "Model 3", "year": 2023}}
            ]
        }
    }
    identity_instance.dimo.query.return_value = mock_response

    address = "0xMockAddress"
    limit = 3
    result = await identity_instance.mmy_by_owner(address, limit)

    assert result == mock_response
    identity_instance.dimo.query.assert_awaited_once_with(
        "Identity",
        """
    query MMYByOwner($owner: Address!, $first: Int!) {
      vehicles(filterBy: {owner: $owner}, first: $first) {
        nodes {
          definition {
            make
            model
            year
          }
        }
      }
    }
    """,
        variables={"owner": address, "first": limit},
    )


@pytest.mark.asyncio
async def test_mmy_by_token_id(identity_instance):
    """
    Tests the mmy_by_token_id method
    """
    # Define a mock response
    mock_response = {
        "vehicle": {"definition": {"make": "Toyota", "model": "Corolla", "year": 2020}}
    }
    identity_instance.dimo.query.return_value = mock_response

    token_id = 1
    result = await identity_instance.mmy_by_token_id(token_id)

    assert result == mock_response
    identity_instance.dimo.query.assert_awaited_once_with(
        "Identity",
        """
      query MMYByTokenID($tokenId: Int!) {
        vehicle (tokenId: $tokenId) {
          aftermarketDevice {
            tokenId
            address
          }
          syntheticDevice {
            tokenId
            address
          }
          definition {
            make
            model
            year
          }
        }
      }
      """,
        variables={"tokenId": token_id},
    )


@pytest.mark.asyncio
async def test_rewards_by_owner(identity_instance):
    """
    Tests the rewards_by_owner method
    """
    # Define a mock response
    mock_response = {"rewards": {"totalTokens": 50}}
    identity_instance.dimo.query.return_value = mock_response

    address = "0xMockAddress"
    result = await identity_instance.rewards_by_owner(address)

    assert result == mock_response
    identity_instance.dimo.query.assert_awaited_once_with(
        "Identity",
        """
      query RewardsByOwner($owner: Address!) {
        rewards (user: $owner) {
          totalTokens
        }
      }
      """,
        variables={"owner": address},
    )


@pytest.mark.asyncio
async def test_rewards_history_by_owner(identity_instance):
    """
    Tests the rewards_history_by_owner method
    """
    # Define a mock response
    mock_response = {
        "vehicles": {
            "nodes": [
                {
                    "earnings": {
                        "history": {
                            "edges": [{"node": {"week": "2023-W01", "tokens": 10}}]
                        }
                    }
                }
            ]
        }
    }
    identity_instance.dimo.query.return_value = mock_response

    address = "0xMockOwner"
    limit = 5
    result = await identity_instance.rewards_history_by_owner(address, limit)

    assert result == mock_response
    identity_instance.dimo.query.assert_awaited_once_with(
        "Identity",
        """
      query GetVehicleDataByOwner($owner: Address!, $first: Int!) {
        vehicles (filterBy: {owner: $owner}, first: $first) {
          nodes {
            earnings {
              history (first: $first) {
                edges {
                  node {
                    week
                    aftermarketDeviceTokens
                    syntheticDeviceTokens
                    sentAt
                    beneficiary
                    connectionStreak
                    streakTokens
                  }
                }
              }
              totalTokens
            }
          }
        }
      }
      """,
        variables={"owner": address, "first": limit},
    )
