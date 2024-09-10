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
    expected = {
        'Пряная дыня с глинтвейном': (
            'https://vkusvill.ru//media/recipes/pryanaya-dynya-s-glintveynom.html'
        )
    }
    print(f"Результат: {result}")
    assert result == expected


@mock.patch('os.path.exists')
@mock.patch('os.mkdir')
@mock.patch('builtins.open', new_callable=mock.mock_open)
def test_directory_creation(mock_open, mock_mkdir, mock_exists):
    mock_exists.return_value = False
    Parser.collect_links(start_page=1, end_page=2)
    call = mock_open.call_args_list
    print(call)
    mock_mkdir.assert_any_call('data/recipe_pages/')
    mock_open.assert_any_call('data/recipe_pages/result_recipe_pages.json', 'a', encoding='utf-8')
    mock_open.assert_any_call('data/recipe_pages/page_1.html', 'w', encoding='utf-8')
    mock_open.assert_any_call('data/recipe_pages/page_1.html', encoding='utf-8')
    assert mock_open.call_count == 3


def test_collect_links_creates_json():
    result = Parser.collect_links(1, 2)
    result_json = json.dumps(result, indent=4, ensure_ascii=False)
    expected_json = json.dumps(
        {
            'Пряная дыня с глинтвейном': (
                'https://vkusvill.ru//media/recipes/pryanaya-dynya-s-glintveynom.html'
            )
        },
        indent=4,
        ensure_ascii=False
    )
    assert expected_json == result_json
    print(f'Expected JSON: {expected_json}')
    print(f'Result JSON: {result_json}')


def test_parse_recipes():
    recipes_dict = Parser.collect_links(1, 2)
    print(recipes_dict)
    result = Parser.parse_recipes(recipes_dict)
    print(result)
    expected = [
        {
            'Пряная дыня с глинтвейном': {
                'Steps': [
                    'Налейте вино в кастрюлю.'
                ],
                'Ingredients': {
                    'дыня плотная': '1 шт. (примерно 500 г)'
                }
            }
        }
    ]
    assert expected == result


def test_parse_recipes_json(mock_request):
    recipes_dict = Parser.collect_links(1, 2)
    result = Parser.parse_recipes(recipes_dict)
    result_json = json.dumps(result, indent=4, ensure_ascii=False)
    print(result_json)
    expected_json = json.dumps(
        [
            {
                'Пряная дыня с глинтвейном': {
                    'Steps': [
                        'Налейте вино в кастрюлю.'
                    ],
                    'Ingredients': {
                        'дыня плотная': '1 шт. (примерно 500 г)'
                    }
                }
            }
        ],
        indent=4,
        ensure_ascii=False
    )
    assert expected_json == result_json


@mock.patch('os.path.exists')
@mock.patch('os.mkdir')
@mock.patch('builtins.open', new_callable=mock.mock_open)
def test_parser_recipes_directory_creation(mock_open, mock_mkdir, mock_exists):
    mock_exists.return_value = False
    recipes_dict = {
        'Пряная дыня с глинтвейном': 'https://vkusvill.ru//media/recipes/pryanaya-dynya-s-glintveynom.html'
    }

    # Запуск парсера
    Parser.parse_recipes(recipes_dict)

    # Проверка, что каталог был создан
    mock_mkdir.assert_called_once_with('data/recipes/')

    # Проверка, что файл для HTML был открыт трижды (для записи и для чтения) + JSON
    assert mock_open.call_count == 3  # Добавляем проверку на 3 вызова open

    # Проверка вызова для записи HTML-файла
    mock_open.assert_any_call('data/recipes/_Пряная_дыня_с_глинтвейном.html', 'w', encoding='utf-8')

    # Проверка вызова для чтения HTML-файла
    mock_open.assert_any_call('data/recipes/_Пряная_дыня_с_глинтвейном.html', encoding='utf-8')

    # Проверка вызова для записи JSON-файла
    mock_open.assert_any_call('data/result_data.json', 'a', encoding='utf-8')
