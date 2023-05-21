from http import HTTPStatus

import pytest

from core.config import settings
from tests.data import api_data


@pytest.mark.parametrize(
    'body_data, expected_answer',
    [({'body': api_data.body},
      {'status': HTTPStatus.OK, 'response': api_data.response}),
     ({'body': 'fake_data'},
      {'status': HTTPStatus.NOT_FOUND, 'response': {'detail': 'No this build.'}}),
     ]
)
@pytest.mark.asyncio
async def test_build_api(make_post_request, body_data, expected_answer):
    body, headers, status = await make_post_request(settings.get_tasks_url, {}, {'build': body_data['body']})
    assert status[0] == expected_answer['status']
    assert body[0] == expected_answer['response']
