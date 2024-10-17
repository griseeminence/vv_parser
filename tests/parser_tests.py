import pytest
import json
import unittest.mock as mock

from parser.core import Parser


def test_correct_request_bs4(collect_links_expected):
    """
    Autouse pytest.fixture "mock request" for request.text and request.status_code
    Autouse pytest.fixture "setup_and_teardown" for delete data directory after tests
    """
    result = Parser.collect_links(1, 2)
    expected = collect_links_expected
    print(f"Результат: {result}")
    print(f"expected: {expected}")
    assert result == expected


@mock.patch('os.path.exists')
@mock.patch('os.mkdir')
@mock.patch('builtins.open', new_callable=mock.mock_open)
def test_directory_creation(mock_open, mock_mkdir, mock_exists):
    mock_exists.return_value = False
    Parser.collect_links(start_page=1, end_page=2)
    mock_mkdir.assert_any_call('data/recipe_pages/')
    mock_open.assert_any_call('data/recipe_pages/result_recipe_pages.json', 'a', encoding='utf-8')
    mock_open.assert_any_call('data/recipe_pages/page_1.html', 'w', encoding='utf-8')
    mock_open.assert_any_call('data/recipe_pages/page_1.html', encoding='utf-8')
    assert mock_open.call_count == 3


def test_collect_links_creates_json(collect_links_expected_json):
    result = Parser.collect_links(1, 2)
    result_json = json.dumps(result, indent=4, ensure_ascii=False)
    expected_json = collect_links_expected_json
    assert expected_json == result_json
    print(f'Expected JSON: {expected_json}')
    print(f'Result JSON: {result_json}')


def test_parse_recipes(parse_recipes_expected):
    recipes_dict = Parser.collect_links(1, 2)
    print(f'recipes_dict: {recipes_dict}')
    result = Parser.parse_recipes(recipes_dict)
    print(f'result: {result}')
    expected = parse_recipes_expected
    print(f'expected: {expected}')
    assert expected == result


def test_parse_recipes_json(mock_request, parse_recipes_expected_json):
    recipes_dict = Parser.collect_links(1, 2)
    result = Parser.parse_recipes(recipes_dict)
    result_json = json.dumps(result, indent=4, ensure_ascii=False)
    print(f'result_json: {result_json}')
    expected_json = parse_recipes_expected_json
    print(f'expected_json: {expected_json}')
    assert expected_json == result_json


@mock.patch('os.path.exists')
@mock.patch('os.mkdir')
@mock.patch('builtins.open', new_callable=mock.mock_open)
def test_parser_recipes_directory_creation(mock_open, mock_mkdir, mock_exists, recipes_dict_example):
    mock_exists.return_value = False
    recipes_dict = recipes_dict_example
    Parser.parse_recipes(recipes_dict)
    mock_mkdir.assert_called_once_with('data/recipes/')
    mock_open.assert_any_call('data/recipes/_Пряная_дыня_с_глинтвейном.html', 'w', encoding='utf-8')
    mock_open.assert_any_call('data/recipes/_Пряная_дыня_с_глинтвейном.html', encoding='utf-8')
    mock_open.assert_any_call('data/result_data.json', 'a', encoding='utf-8')
    assert mock_open.call_count == 3


def test_start_parser(parse_recipes_expected):
    result = Parser.start_parser(1, 2)
    expected = parse_recipes_expected
    assert expected == result
