from pydantic import validator

from models.orjson_model import OrJsonModel
from services.file_service import builds_list


class TaskModel(OrJsonModel):
    name: str
    dependencies: list


class BuildModel(OrJsonModel):
    name: str
    tasks: list


class RequestBuildModel(OrJsonModel):
    builds: list = builds_list
    build: str

    @validator('build')
    def match_build(cls, v):
        if v not in cls.builds:
            raise ValueError('There is no such build, verify builds.yaml')
        return v

class TasksResponse(OrJsonModel):
    __root__: list[str]
