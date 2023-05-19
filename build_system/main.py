from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.logger import logging
from services import file_service as fs

logger = logging.getLogger(__name__)

# app = FastAPI(
#     title='Build System',
#     docs_url='/build_sys/api/openapi',
#     openapi_url='/build_sys/api/openapi.json',
#     default_response_class=ORJSONResponse,
# )
 
data = fs.builds_list
print(data)
data2 = fs.tasks_list
print(data2)
