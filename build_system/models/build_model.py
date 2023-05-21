from models.orjson_model import OrJsonModel


class BodyBuildModel(OrJsonModel):
    build: str


class TasksResponse(OrJsonModel):
    __root__: list[str]
