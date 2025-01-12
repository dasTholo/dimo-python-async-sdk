from dimo.errors import check_type


class Valuations:
    def __init__(self, request_method, get_auth_headers):
        self._request = request_method
        self._get_auth_headers = get_auth_headers

    async def get_valuations(self, vehicle_jwt: str, token_id: int) -> dict:
        check_type("vehicle_jwt", vehicle_jwt, str)
        check_type("token_id", token_id, int)
        url = f"/v2/vehicles/{token_id}/valuations"
        return await self._request(
            "GET", "Valuations", url, headers=self._get_auth_headers(vehicle_jwt)
        )

    async def offers_lookup(self, vehicle_jwt: str, token_id: int) -> None:
        check_type("vehicle_jwt", vehicle_jwt, str)
        check_type("token_id", token_id, int)
        url = f"v2/vehicles/{token_id}/instant-offer"
        return await self._request(
            "GET", "Valuations", url, headers=self._get_auth_headers(vehicle_jwt)
        )

    async def list_vehicle_offers(self, vehicle_jwt: str, token_id: int) -> dict:
        check_type("vehicle_jwt", vehicle_jwt, str)
        check_type("token_id", token_id, int)
        url = f"/v2/vehicles/{token_id}/offers"
        return await self._request(
            "GET", "Valuations", url, headers=self._get_auth_headers(vehicle_jwt)
        )
