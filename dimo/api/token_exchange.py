from dimo.constants import dimo_constants
from dimo.errors import check_type


class TokenExchange:

    def __init__(self, request_method, get_auth_headers):
        self._request = request_method
        self._get_auth_headers = get_auth_headers

    async def exchange(
        self,
        developer_jwt: str,
        privileges: list,
        token_id: int,
        env: str = "Production",
    ) -> dict:
        check_type("developer_jwt", developer_jwt, str)
        check_type("privileges", privileges, list)
        check_type("token_id", token_id, int)
        body = {
            "nftContractAddress": dimo_constants[env]["NFT_address"],
            "privileges": privileges,
            "tokenId": token_id,
        }
        response = await self._request(
            "POST",
            "TokenExchange",
            "/v1/tokens/exchange",
            headers=self._get_auth_headers(developer_jwt),
            data=body,
        )
        return response
