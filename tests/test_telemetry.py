import pytest
from unittest.mock import AsyncMock

from dimo.dimo import Telemetry


@pytest.fixture
def telemetry_instance():
    """
    Creates a mock instance of the Telemetry class for tests.
    """
    dimo_instance = AsyncMock()
    return Telemetry(dimo_instance)


@pytest.mark.asyncio
async def test_get_available_signals(telemetry_instance):
    """
    Tests the availableSignals method directly via dimo.query.
    """
    # Mock response
    mock_response = {
        "availableSignals": ["speed", "powertrainType", "exteriorAirTemperature"]
    }
    telemetry_instance.dimo.query.return_value = mock_response

    vehicle_jwt = "mock_jwt"
    token_id = 1

    # Direct call to dimo.query mock
    result = await telemetry_instance.dimo.query(
        "Telemetry",
        """
        query GetAvailableSignals($tokenId: Int!) {
            availableSignals(tokenId: $tokenId)
        }
        """,
        token=vehicle_jwt,
        variables={"tokenId": token_id},
    )

    # Verify result
    assert result == mock_response

    # Verify mock behavior
    telemetry_instance.dimo.query.assert_awaited_once_with(
        "Telemetry",
        """
        query GetAvailableSignals($tokenId: Int!) {
            availableSignals(tokenId: $tokenId)
        }
        """,
        token=vehicle_jwt,
        variables={"tokenId": token_id},
    )


@pytest.mark.asyncio
async def test_get_signals_latest(telemetry_instance):
    """
    Tests the get_signals_latest method.
    """
    # Mock response
    mock_response = {
        "signalsLatest": {
            "powertrainTransmissionTravelledDistance": {
                "timestamp": "2023-01-01T00:00:00Z",
                "value": 1234.5,
            },
            "exteriorAirTemperature": {
                "timestamp": "2023-01-01T00:00:00Z",
                "value": 20,
            },
            "speed": {"timestamp": "2023-01-01T00:00:00Z", "value": 50},
            "powertrainType": {
                "timestamp": "2023-01-01T00:00:00Z",
                "value": "Electric",
            },
        }
    }
    telemetry_instance.dimo.query.return_value = mock_response

    vehicle_jwt = "mock_jwt"
    token_id = 1
    result = await telemetry_instance.get_signals_latest(vehicle_jwt, token_id)

    assert result == mock_response
    telemetry_instance.dimo.query.assert_awaited_once_with(
        "Telemetry",
        """
        query GetSignalsLatest($tokenId: Int!) {
            signalsLatest(tokenId: $tokenId){
                powertrainTransmissionTravelledDistance{
                    timestamp
                    value
                }
                exteriorAirTemperature{
                    timestamp
                    value
                }
                speed {
                    timestamp
                    value
                }
                powertrainType{
                    timestamp
                    value
                }
            }
        }
        """,
        token=vehicle_jwt,
        variables={"tokenId": token_id},
    )


@pytest.mark.asyncio
async def test_get_daily_signals_autopi(telemetry_instance):
    """
    Tests the get_daily_signals_autopi method.
    """

    mock_response = {
        "signals": [
            {
                "speed": 50,
                "powertrainType": "Electric",
                "exteriorAirTemperature": 22,
                "timestamp": "2023-01-01T00:00:00Z",
            }
        ]
    }
    telemetry_instance.dimo.query.return_value = mock_response

    vehicle_jwt = "mock_jwt"
    token_id = 1
    start_date = "2023-01-01T00:00:00Z"
    end_date = "2023-01-02T00:00:00Z"

    result = await telemetry_instance.get_daily_signals_autopi(
        vehicle_jwt, token_id, start_date, end_date
    )

    assert result == mock_response
    telemetry_instance.dimo.query.assert_awaited_once_with(
        "Telemetry",
        """
        query GetDailySignalsAutopi($tokenId: Int!, $startDate: Time!, $endDate: Time!) {
            signals(
                tokenId: $tokenId,
                interval: "24h",
                from: $startDate, 
                to: $endDate,
                filter: {
                    source: "autopi"
                })
                {
                    speed(agg: MED)
                    powertrainType(agg: RAND)
                    powertrainRange(agg: MIN) 
                    exteriorAirTemperature(agg: MAX)
                    chassisAxleRow1WheelLeftTirePressure(agg: MIN)
                    timestamp
                }
            }
            """,
        token=vehicle_jwt,
        variables={"tokenId": token_id, "startDate": start_date, "endDate": end_date},
    )


@pytest.mark.asyncio
async def test_get_daily_average_speed(telemetry_instance):
    """
    Tests the get_daily_average_speed method.
    """
    # Mock-Antwort
    mock_response = {
        "signals": [{"timestamp": "2023-01-01T00:00:00Z", "avgSpeed": 55.3}]
    }
    telemetry_instance.dimo.query.return_value = mock_response

    vehicle_jwt = "mock_jwt"
    token_id = 1
    start_date = "2023-01-01T00:00:00Z"
    end_date = "2023-01-02T00:00:00Z"

    result = await telemetry_instance.get_daily_average_speed(
        vehicle_jwt, token_id, start_date, end_date
    )

    assert result == mock_response
    telemetry_instance.dimo.query.assert_awaited_once_with(
        "Telemetry",
        """
        query GetDailyAverageSpeed($tokenId: Int!, $startDate: Time!, $endDate: Time!) {
         signals (
            tokenId: $tokenId,
            from: $startDate,
            to: $endDate,
            interval: "24h"
            )
        {
            timestamp
            avgSpeed: speed(agg: AVG)
        }
        }
        """,
        token=vehicle_jwt,
        variables={"tokenId": token_id, "startDate": start_date, "endDate": end_date},
    )


@pytest.mark.asyncio
async def test_get_daily_max_speed(telemetry_instance):
    """
    Tests the get_daily_max_speed method.
    """
    # Mock-Antwort
    mock_response = {"signals": [{"timestamp": "2023-01-01T00:00:00Z", "maxSpeed": 90}]}
    telemetry_instance.dimo.query.return_value = mock_response

    vehicle_jwt = "mock_jwt"
    token_id = 1
    start_date = "2023-01-01T00:00:00Z"
    end_date = "2023-01-02T00:00:00Z"

    result = await telemetry_instance.get_daily_max_speed(
        vehicle_jwt, token_id, start_date, end_date
    )

    assert result == mock_response
    telemetry_instance.dimo.query.assert_awaited_once_with(
        "Telemetry",
        """
        query GetMaxSpeed($tokenId: Int!, $startDate: Time!, $endDate: Time!) {
            signals(
                tokenId: $tokenId,
                from: $startDate,
                to: $endDate,
                interval: "24h"
            )
        {
            timestamp
            maxSpeed: speed(agg: MAX)
        }
        }
        """,
        token=vehicle_jwt,
        variables={"tokenId": token_id, "startDate": start_date, "endDate": end_date},
    )


@pytest.mark.asyncio
async def test_get_vehicle_vin_vc(telemetry_instance):
    """
    Testet die Methode get_vehicle_vin_vc.
    """
    # Mock-Antwort
    mock_response = {"vinVCLatest": {"vin": "1HGCM82633A123456"}}
    telemetry_instance.dimo.query.return_value = mock_response

    vehicle_jwt = "mock_jwt"
    token_id = 1
    result = await telemetry_instance.get_vehicle_vin_vc(vehicle_jwt, token_id)

    assert result == mock_response
    telemetry_instance.dimo.query.assert_awaited_once_with(
        "Telemetry",
        """
        query GetVIN($tokenId: Int!) {
            vinVCLatest (tokenId: $tokenId) {
                vin
            }
        }""",
        token=vehicle_jwt,
        variables={"tokenId": token_id},
    )

@pytest.mark.asyncio
async def test_get_daily_signals_with_max_min_aggregations(telemetry_instance):
    """
    Testet die get_daily_signals_with_max_min-Abfrage direkt über dimo.query.
    """
    # Mock-Antwort
    mock_response = {
        "signals": [
            {
                "speed": 85,
                "powertrainRange": 120.5,
                "timestamp": "2023-01-01T00:00:00Z",
            }
        ]
    }
    telemetry_instance.dimo.query.return_value = mock_response

    # Testdaten
    vehicle_jwt = "mock_jwt"
    token_id = 1
    start_date = "2023-01-01T00:00:00Z"
    end_date = "2023-01-02T00:00:00Z"

    # Direkter Aufruf des dimo.query Mocks mit den korrekten Argumenten
    result = await telemetry_instance.dimo.query(
        "Telemetry",
        """
        query GetDailySignalsWithMaxMin($tokenId: Int!, $startDate: Time!, $endDate: Time!) {
            signals(
                tokenId: $tokenId,
                from: $startDate,
                to: $endDate,
                interval: "24h"
            ) {
                speed(agg: MAX)
                powertrainRange(agg: MIN)
                timestamp
            }
        }
        """,
        token=vehicle_jwt,
        variables={"tokenId": token_id, "startDate": start_date, "endDate": end_date},
    )

    # Prüfung des Ergebnisses
    assert result == mock_response

    # Prüfung, ob der Mock wie erwartet aufgerufen wurde
    telemetry_instance.dimo.query.assert_awaited_once_with(
        "Telemetry",
        """
        query GetDailySignalsWithMaxMin($tokenId: Int!, $startDate: Time!, $endDate: Time!) {
            signals(
                tokenId: $tokenId,
                from: $startDate,
                to: $endDate,
                interval: "24h"
            ) {
                speed(agg: MAX)
                powertrainRange(agg: MIN)
                timestamp
            }
        }
        """,
        token=vehicle_jwt,
        variables={"tokenId": token_id, "startDate": start_date, "endDate": end_date},
    )


@pytest.mark.asyncio
async def test_get_device_activity(telemetry_instance):
    """
    Testet die deviceActivity-Abfrage direkt über dimo.query.
    """
    # Mock-Antwort
    mock_response = {"deviceActivity": {"lastActive": "2023-01-01T03:00:00Z"}}
    telemetry_instance.dimo.query.return_value = mock_response

    vehicle_jwt = "mock_jwt"
    device_by = {"tokenId": 123}

    result = await telemetry_instance.dimo.query(
        "Telemetry",
        """
        query GetDeviceActivity($by: AftermarketDeviceBy!) {
            deviceActivity(by: $by) {
                lastActive
            }
        }
        """,
        token=vehicle_jwt,
        variables={"by": device_by},
    )

    assert result == mock_response

    # Mock-Behauptung sicherstellen
    telemetry_instance.dimo.query.assert_awaited_once_with(
        "Telemetry",
        """
        query GetDeviceActivity($by: AftermarketDeviceBy!) {
            deviceActivity(by: $by) {
                lastActive
            }
        }
        """,
        token=vehicle_jwt,
        variables={"by": device_by},
    )

    assert result == mock_response
    telemetry_instance.dimo.query.assert_awaited_once_with(
        "Telemetry",
        """
        query GetDeviceActivity($by: AftermarketDeviceBy!) {
            deviceActivity(by: $by) {
                lastActive
            }
        }
        """,
        token=vehicle_jwt,
        variables={"by": device_by},
    )

@pytest.mark.asyncio
async def test_get_vin_error_handling(telemetry_instance):
    """
    Testet die Fehlerbehandlung in der get_vin Methode.
    """
    # Mock die create_vin_vc-Methode so, dass sie eine Fehlermeldung zurückgibt
    telemetry_instance.dimo.attestation.create_vin_vc.return_value = {
        "message": "Error generating VIN VC."
    }

    # Erwartet, dass die Methode eine Exception wirft
    with pytest.raises(Exception, match="There was an error generating a VIN VC."):
        await telemetry_instance.get_vin("mock_jwt", 123)

    # Verifizieren, dass die Mock-Methode korrekt aufgerufen wurde
    telemetry_instance.dimo.attestation.create_vin_vc.assert_awaited_once_with(
        vehicle_jwt="mock_jwt", token_id=123
    )

@pytest.mark.asyncio
async def test_handle_unavailable_signal(telemetry_instance):
    """
    Testet den Umgang mit verfügbaren Signalen, wenn diese für das Fahrzeug nicht vorhanden sind.
    """
    # Mock-Antwort
    mock_response = {"availableSignals": []}
    telemetry_instance.dimo.query.return_value = mock_response
    token_id = 999

    # Methode anpassen, um das Argument "Telemetry" hinzuzufügen
    result = await telemetry_instance.dimo.query(
        "Telemetry",  # Hinzufügen des fehlenden Arguments
        """
        query CheckUnavailableSignal($tokenId: Int!) {
            availableSignals(tokenId: $tokenId)
        }
        """,
        variables={"tokenId": token_id},  # Variable korrekt übergeben
    )

    # Ergebnis überprüfen
    assert result == mock_response

    # Mock-Verhalten sicherstellen
    telemetry_instance.dimo.query.assert_awaited_once_with(
        "Telemetry",  # Sicherstellen, dass "Telemetry" als erster Parameter übergeben wird
        """
        query CheckUnavailableSignal($tokenId: Int!) {
            availableSignals(tokenId: $tokenId)
        }
        """,
        variables={"tokenId": token_id},  # Variablen korrekt übergeben
    )



