from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from models.build_model import BodyBuildModel, TasksResponse
from services.api_service import APIService, get_api_service
from services.data_service import full_data

router = APIRouter()


@router.post('/get_tasks')
async def get_tasks(
        body: BodyBuildModel,
        builds_service: APIService = Depends(get_api_service)
    ) -> TasksResponse:
    if body.build not in full_data.data_file.list_builds:
        HTTPException(HTTPStatus.NOT_FOUND, 'No this build.')
    return await builds_service.get_tasks_by_build(body)
