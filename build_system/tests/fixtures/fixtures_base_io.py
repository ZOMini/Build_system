import asyncio
from typing import AsyncIterator

import aiohttp
import pytest
import pytest_asyncio


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def ahttp_client() -> AsyncIterator[aiohttp.ClientSession]:
    session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=35, loop=asyncio.get_event_loop()))
    yield session
    await session.close()
