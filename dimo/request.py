import orjson
from httpx import AsyncClient


class AsyncRequest:

    def __init__(self, http_method, url):
        self.http_method = http_method
        self.url = url
        self.client = AsyncClient()

    async def __call__(self, headers=None, data=None, params=None, **kwargs):
        headers = headers or {}
        headers.update(kwargs.pop("headers", {}))

        if (
            data
            and isinstance(data, dict)
            and headers.get("Content-Type") == "application/json"
        ):
            data = orjson.dumps(data)

        # Perform the async request
        response = await self.client.request(
            method=self.http_method,
            url=self.url,
            headers=headers,
            params=params,
            data=data,
            **kwargs,
        )

        # TODO: Better error responses
        response.raise_for_status()

        if response.content:
            return orjson.loads(response.content)
        return None
