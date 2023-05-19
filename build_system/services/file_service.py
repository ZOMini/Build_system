import asyncio

import aiofiles
import yaml

from core.config import settings
from core.logger import logging

logger = logging.getLogger(__name__)


async def read_file(name: str):
    async with aiofiles.open(f'{settings.files_path}{name}') as f:
        _f = await f.read()
        read_data = yaml.safe_load(_f)
        return read_data

async def read_files() -> tuple[dict, dict]:
    async with asyncio.TaskGroup() as tg:
        read_tasks = tg.create_task(read_file('tasks.yaml'))
        read_builds = tg.create_task(read_file('builds.yaml'))
    return await read_builds, await read_tasks

builds, tasks = asyncio.run(read_files())

def list_builds() -> list[str]:
    return [b['name'] for b in builds['builds']]

def list_tasks() -> list[str]:
    return [t['name'] for t in tasks['tasks']]

builds_list, tasks_list = list_builds(), list_tasks()
