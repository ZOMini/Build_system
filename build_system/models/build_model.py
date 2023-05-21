from models.orjson_model import OrJsonModel


class BodyBuildModel(OrJsonModel):
    build: str

    class Config:
        schema_extra = {
            "example": {
                "build": "forward_interest",
            }
        }


class TasksResponse(OrJsonModel):
    __root__: list[str]

    class Config:
        schema_extra = {
            "example": [
                "design_green_ogres",
                "create_maroon_ogres",
                "build_yellow_ogres",
                "bring_green_ogres",]
        }


class Response_404(OrJsonModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {
                "detail": "No this build.",
            }
        }
