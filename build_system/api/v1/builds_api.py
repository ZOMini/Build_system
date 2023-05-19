from fastapi import APIRouter, Depends

from models.build_model import RequestBuildModel, TasksResponse
from services.api_service import APIService, get_api_service

router = APIRouter()


@router.post('/get_tasks')
async def get_tasks(
    build: RequestBuildModel,
    billing_service: APIService = Depends(get_api_service)
    ) -> TasksResponse:
    pass
