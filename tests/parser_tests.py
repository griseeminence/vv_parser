import pytest

import main
from main import Parser
import unittest.mock as mock


@mock.patch('main.Parser')
def test_request(mock_request):
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'status': 'OK'}
    mock_request.return_value = mock_response
    data = main.Parser.collect_links(1, 2)
    assert data == {'status': 'OK'}
