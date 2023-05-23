import asyncio
import time
from typing import Any

import aiofiles
import yaml


class FileAIO():
    
    @classmethod
    async def read_file(cls, name: str, *args, **kwargs) -> dict:
        async with aiofiles.open(f'./builds/{name}', mode='r', *args, **kwargs) as f:
            _f = await f.read()
            read_data = yaml.safe_load(_f)
            return read_data

    @classmethod
    async def read_files(cls, list_files_names: list[str]) -> tuple:
        result = []
        dict_tasks: dict[str, asyncio.Task] = {}
        async with asyncio.TaskGroup() as tg:
            for file_name in list_files_names:
                task = tg.create_task(cls.read_file(file_name), name=file_name)
                dict_tasks[file_name] = task
        for file_name in list_files_names:
            result.append(dict_tasks[file_name].result())
        return tuple(result)

    @classmethod
    async def read_files_wo_tasks(cls, list_files_names: list[str]) -> dict[str, Any]:
        result = {}
        for file_name in list_files_names:
            result[file_name] = await cls.read_file(file_name)
        return result

st = time.time()
work_list = ['builds.yaml', 'tasks.yaml']
res = asyncio.run(FileAIO.read_files(work_list))
for file in res:
    print(file)

# def sync_files():
#     import os
#     work_dict = {}
#     for name in work_list:
#         path = f"builds/{name}"
#         # assert os.path.isfile(path)
#         with open(path, 'r') as f:
#             # _f = f.read()
#             work_dict[name] = yaml.safe_load(f)
#     return work_dict

# work_dict = sync_files()
# for i in work_list:
#     print(work_dict[i])

ft = time.time()
print(f'deltatime {ft - st}')
