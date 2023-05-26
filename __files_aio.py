# Файл для опытов:).
import asyncio
import logging
import time
from typing import Any

import aiofiles
import networkx as nx
import yaml
from yaml import CFullLoader

WORK_DICT = {'builds': 'tasks', 'tasks': 'dependencies'}
FILE_DIR = './builds/'

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class FileAIO:

    @classmethod
    async def read_file(self, name: str, **kwargs) -> Any:
        file_path = f'{FILE_DIR}{name}.yaml'
        async with aiofiles.open(file_path, mode='r', **kwargs) as f:
            _f = await f.read()
            read_data = yaml.load(_f, CFullLoader)
            return read_data

    @classmethod
    async def read_files(self) -> dict[str, list[dict]]:
        result = {}
        for file_name in WORK_DICT:
            result.update(await self.read_file(file_name))
        return result


class FileData():
    """@DynamicAttrs"""

    __slot__ = tuple(WORK_DICT)

    def __init__(self, data: dict[str, list[dict]]) -> None:
        for k, v in data.items():
            setattr(self, k, self.convert_to_dict(v, WORK_DICT[k]))

    def __getattr__(self, name: str) -> Any:
        return self.__getattribute__(name)

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def convert_to_dict(self, list_data: list[dict], value: str) -> dict:
        result = {}
        for d in list_data:
            result[d['name']] = d[value]
        return result

    def check_cyclic_dependencies(self) -> None:
        '''Проверяет на циклические зависимости таски + билды,
        на все глубину, возможно излишне.
        Возможно достаточно было проверять только по действующим билдам,
        но сделано по полной.'''
        full_dict = {WORK_DICT[d]: getattr(self, d) for d in WORK_DICT}
        graph = nx.DiGraph(full_dict)
        list_err = list(nx.simple_cycles(graph))
        if list_err:
            raise ValueError(f'Cyclic dependencies have been found - {list_err}')
        logger.warning('There are no cyclic references.')


class WorkFileData(FileData):

    def __init__(self, data: dict[str, list[dict]]) -> None:
        super().__init__(data)
        self.builds: dict[str, list[dict]]
        self.tasks: dict[str, list[dict]]

    @property
    def list_builds(self):
        return [b for b in self.builds.keys()]

    @property
    def list_tasks(self):
        return [t for t in self.tasks.keys()]

    @property
    def builds_responses(self):
        return self.builds_full_dependences()

    def full_dependences(self, name: str, full_list: list, build=False) -> list:
        """Рекурсия для получения зависимостей на всю глубину."""
        work_list: list = self.builds[name] if build else self.tasks[name]
        if work_list:
            full_list = full_list + work_list
            for task_name in work_list:
                full_list = self.full_dependences(task_name, full_list)
        return full_list

    def remove_duplicates(self, data: list) -> list:
        """Удаляем дубликаты task-ов(хотя из задания не понятно - нужно ли удалять).
        Через словарь чуть быстрее, чем через set() или иные варианты."""
        return list(dict.fromkeys(data))

    def builds_full_dependences(self) -> dict[str, list[str]]:
        """Метод формирует готовые билды для отправки.
        Этим же методом можно формировать полные зависимости для тасков,
        но не понадобилось, возможность оставил."""
        data_dict = {}
        for item in self.list_builds:
            item_full_dep = self.full_dependences(item, [], True)
            item_full_dep.reverse()
            # Если не нужно удалять дубликаты тасков, то убрать следующюю строку.
            item_full_dep = self.remove_duplicates(item_full_dep)
            data_dict[item] = item_full_dep
        return data_dict


def init_data():
    st = time.time()
    file = asyncio.run(FileAIO.read_files())
    work_file_data = WorkFileData(file)
    work_file_data.check_cyclic_dependencies()
    logger.warning(f'init deltatime {time.time() - st}')
    return work_file_data.builds_responses


builds_responses = init_data()


class Aa:

    def __init__(self, a1: str, a2: str):
        self.a1 = a1
        self.a2 = a2

    @property
    def list_a(self):
        return [self.a1, self.a2]

    @list_a.setter
    def list_a(self, set_dict: dict) -> None:
        for name, value in set_dict.items():
            setattr(self, name, value)


aa = Aa('a1', 'a2')
print(aa.list_a)
aa.list_a = {'a1': 'a11', 'a2': 'a22'}
print(aa.list_a)
