import pytest
# from unittest.mock import patch, mock_open
import unittest.mock as mock
import os
import json

import requests

from main import Parser


# TODO: определить в класс, вывести doc строку в коммент к классу (про autouse)
def test_correct_request_bs4():
    """
    Autouse pytest.fixture "mock request" for request.text and request.status_code
    Autouse pytest.fixture "setup_and_teardown" for delete data directory after tests
    """
    result = Parser.collect_links(1, 2)
    expected = {'Пряная дыня с глинтвейном': 'https://vkusvill.ru//media/recipes/pryanaya-dynya-s-glintveynom.html'}
    print(f"Результат: {result}")
    assert result == expected


@mock.patch('os.path.exists')
@mock.patch('os.mkdir')
def test_directory_creation(mock_mkdir, mock_exists):
    mock_exists.return_value = False
    Parser.collect_links(start_page=1, end_page=2)
    mock_mkdir.assert_any_call('data/recipe_pages/')


def test_collect_links_creates_json():
    result = Parser.collect_links(1, 2)
    result_json = json.dumps(result, indent=4, ensure_ascii=False)
    expected_json = json.dumps({
        'Пряная дыня с глинтвейном': 'https://vkusvill.ru//media/recipes/pryanaya-dynya-s-glintveynom.html'
    }, indent=4, ensure_ascii=False)
    assert expected_json == result_json
    print(f'Expected JSON: {expected_json}')
    print(f'Result JSON: {result_json}')
