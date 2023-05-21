from http import HTTPStatus

from models.build_model import Response_404

RESPONSE_404 = {HTTPStatus.NOT_FOUND: {'model': Response_404}}
EXCEPTION_404 = (HTTPStatus.NOT_FOUND, 'No this build.')
