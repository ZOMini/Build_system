import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1 import builds
from core.config import settings
from core.logger import LOGGING

app = FastAPI(
    title='Build System',
    docs_url='/build/api/openapi',
    openapi_url='/build/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(builds.router, prefix='/build/api/v1', tags=['builds'])

if __name__ == '__main__':
    uvicorn.run('main:app',
                host='0.0.0.0',
                port=int(settings.app_port),
                limit_max_requests=128,
                log_level=logging.INFO,
                workers=1,
                reload=False,
                access_log=True,
                log_config=LOGGING)
