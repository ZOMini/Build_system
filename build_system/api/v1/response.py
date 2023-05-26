from http import HTTPStatus

from models.build_model import Response_404

response_404 = {HTTPStatus.NOT_FOUND: {'model': Response_404}}
exception_404 = (HTTPStatus.NOT_FOUND, 'No this build.')

