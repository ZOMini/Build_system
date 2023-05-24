import asyncio
import time
from typing import Any

import aiofile
import aiofiles
import yaml
from yaml import CFullLoader

WORK_DICT = {'builds': 'tasks', 'tasks': 'dependencies'}
FILE_DIR = './builds/'


class FileAIO():
    @classmethod
    async def _read_file(cls, name: str, **kwargs) -> Any:
        """Альтернативный метод, но чуть медленее."""
        file_path = f'{FILE_DIR}{name}.yaml'
        async with aiofile.async_open(file_path, mode='r', **kwargs) as f:
            _f = await f.read()
            read_data = yaml.load(_f, CFullLoader)
            return read_data

    @classmethod
    async def read_file(cls, name: str, **kwargs) -> Any:
        file_path = f'{FILE_DIR}{name}.yaml'
        async with aiofiles.open(file_path, mode='r', **kwargs) as f:
            _f = await f.read()
            read_data = yaml.load(_f, CFullLoader)
            return read_data

    @classmethod
    async def _read_files(cls) -> dict[str, list[dict]]:
        """Альтернативный метод, но беcполезный."""
        result = {}
        dict_tasks: dict[str, asyncio.Task] = {}
        async with asyncio.TaskGroup() as tg:
            for file_name in WORK_DICT:
                task = tg.create_task(cls._read_file(file_name), name=file_name)
                dict_tasks[file_name] = task
        for file_name in WORK_DICT:
            result.update(dict_tasks[file_name].result())
        return result

    @classmethod
    async def read_files(cls) -> dict[str, list[dict]]:
        result: dict[str, list[dict]] = {}
        for file_name in WORK_DICT:
            result.update(await cls.read_file(file_name))
        return result


class FileData():
    __slots__ = tuple(WORK_DICT)

    def __init__(self, data: dict[str, list[dict]]) -> None:
        for k, v in data.items():
            setattr(self, k, self.convert_to_dict(v, WORK_DICT[k]))

    def __getattr__(self, name: str) -> str:
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def convert_to_dict(self, list_data: list[dict], value: str) -> dict:
        result = {}
        for d in list_data:
            result[d['name']] = d[value]
        return result


st = time.time()
file = asyncio.run(FileAIO._read_files())
file_data = FileData(file)
print(f'deltatime {time.time() - st}')
