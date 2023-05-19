import asyncio
import datetime
from pprint import pprint as pp

import aiofiles
import yaml

PATH_TO_FILES = './builds/'


async def read_file(name: str):
    async with aiofiles.open(f'{PATH_TO_FILES}{name}') as f:
        _f = await f.read()
        read_data = yaml.safe_load(_f)
        return read_data

async def read_files():
    async with asyncio.TaskGroup() as tg:
        read_tasks = tg.create_task(read_file('tasks.yaml'))
        read_builds = tg.create_task(read_file('builds.yaml'))
    return await read_builds, await read_tasks

builds, tasks = asyncio.run(read_files())
