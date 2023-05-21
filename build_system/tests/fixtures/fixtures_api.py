import aiohttp
import pytest_asyncio


@pytest_asyncio.fixture
def make_post_request(ahttp_client: aiohttp.ClientSession):
    async def inner(url: str, query: dict, data: dict):
        async with ahttp_client.post(url, params=query, json=data) as response:
            body = await response.json(),
            headers = response.headers,
            status = response.status,
            return body, headers, status
    return inner
