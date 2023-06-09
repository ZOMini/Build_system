from fastapi import APIRouter, Depends, HTTPException

from api.v1 import responses
from models.build_model import BodyBuildModel, TasksResponse
from services.api_service import APIService, get_api_service
from services.data_service import full_data

router = APIRouter()


@router.post('/get_tasks', responses=responses.RESPONSE_404)  # type: ignore
async def get_tasks(
    body: BodyBuildModel,
    builds_service: APIService = Depends(get_api_service)
) -> TasksResponse:
    if body.build not in full_data.keys():
        raise HTTPException(*responses.EXCEPTION_404)
    resp = await builds_service.get_tasks_by_build(body)
    return TasksResponse(__root__=resp)
