import asyncio
import time

import aiofiles
import networkx as nx
import yaml

from core.config import settings
from core.logger import logger


class FileIO():
    @classmethod
    async def read_file(cls, name: str) -> dict:
        async with aiofiles.open(f'{settings.files_path}{name}') as f:
            _f = await f.read()
            read_data = yaml.safe_load(_f)
            return read_data

    @classmethod
    async def read_files(cls) -> tuple[dict, dict]:
        async with asyncio.TaskGroup() as tg:
            read_tasks = tg.create_task(cls.read_file('tasks.yaml'))
            read_builds = tg.create_task(cls.read_file('builds.yaml'))
        return await read_builds, await read_tasks


class FileData():
    def __init__(self, builds, tasks):
        self.builds = self.convert_to_dict(builds['builds'], 'tasks')
        self.tasks = self.convert_to_dict(tasks['tasks'], 'dependencies')

    @property
    def list_builds(self) -> list[str]:
        return [b for b in self.builds.keys()]

    @property
    def list_tasks(self) -> list[str]:
        return [t for t in self.tasks.keys()]

    def convert_to_dict(self, list_data: list[dict], value: str) -> dict[str, list]:
        result = {}
        for d in list_data:
            result[d['name']] = d[value]
        return result

    def check_cyclic_dependencies(self) -> None:
        '''Проверяет на циклические зависимости таски + билды,
        на все глубину, возможно излишне.
        Возможно достаточно было проверять только по действующим билдам,
        но сделано по полной. Да и рекурсия захлебнется, придется шаманить.'''
        graph = nx.DiGraph(self.builds | self.tasks)
        list_err = list(nx.simple_cycles(graph))
        if list_err:
            raise ValueError(f'Detect cyclic dependencies - {list_err}')
        logger.info('There are no cyclic references.')

    def full_dependences(self, name: str, full_list: list, build=False) -> list:
        work_list = self.builds[name] if build else self.tasks[name]
        if work_list:
            full_list = full_list + work_list
            for task_name in work_list:
                full_list = self.full_dependences(task_name, full_list)
        return full_list


class FullData():
    def __init__(self, data_file: FileData) -> None:
        self.data_file = data_file
        self.build_full_dependences = self.all_data_full_dependences()

    def remove_duplicates(self, data: list) -> list:
        """Удаляем дубликаты task-ов(хотя из задания не понятно - нужно ли удалять).
        Через словарь чуть быстрее, чем через set() или иные варианты."""
        return list(dict.fromkeys(data))

    def all_data_full_dependences(self, build=True) -> dict[str, list]:
        """Метод формирует готовые билды для отправки.
        Этим же методом можно формировать полные зависимости для тасков,
        но не понадобилось, возможность оставил."""
        data_dict = {}
        work_array = self.data_file.list_builds if build else self.data_file.list_tasks
        for item in work_array:
            item_full_dep = self.data_file.full_dependences(item, [], build)
            item_full_dep.reverse()
            # Если не нужно удалять дубликаты тасков, то убрать следующюю строку.
            item_full_dep = self.remove_duplicates(item_full_dep)
            data_dict[item] = item_full_dep
        return data_dict


def data_init() -> FullData:
    st = time.time()
    builds, tasks = asyncio.run(FileIO.read_files())
    data_file = FileData(builds, tasks)
    data_file.check_cyclic_dependencies()
    full_data = FullData(data_file)
    ft = time.time()
    logger.info('Init time - %s sec.', ft - st)
    return full_data


full_data = data_init()
