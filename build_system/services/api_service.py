from functools import lru_cache

from core.logger import logging
from models.build_model import BodyBuildModel
from services.data_service import full_data

logger = logging.getLogger(__name__)


class APIService():

    async def get_tasks_by_build(self, build: BodyBuildModel) -> list[str]:
        return full_data.build_full_dependences[build.build]


@lru_cache()
def get_api_service() -> APIService:
    return APIService()
