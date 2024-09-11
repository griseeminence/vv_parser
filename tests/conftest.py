import json
import os
import shutil
import unittest.mock as mock
import pytest

from parser.core import Parser



@pytest.fixture(autouse=True)
def mock_request():
    with mock.patch('requests.get') as mock_request:
        mock_request.status_code = 200
        mock_request.return_value.text = (
            '<html><body>'
            '<a href="/media/recipes/pryanaya-dynya-s-glintveynom.html" '
            'data-news-id="5584103" class="VV_NewsCard__Layout" '
            'aria-label="Пряная дыня с&nbsp;глинтвейном"></a>'
            '<div class="VV_RecipeDetailIng__Col _name" itemprop="recipeIngredient">дыня плотная</div>'
            '<div class="VV_RecipeDetailIng__Col _val b500">1 шт. (примерно 500 г)</div>'
            '<div class="VV_RecipeDetailSteps__StepSubtitle body_article" data-step="1" itemprop="text">Налейте вино в&nbsp;кастрюлю.</div>'
            '</body></html>'
        )
        yield mock_request


@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Создаем папку data перед выполнением тестов
    os.makedirs('data/recipe_pages', exist_ok=True)
    # Выполнение теста
    yield
    # Удаляем папку data после выполнения тестов
    if os.path.exists('data'):
        shutil.rmtree('data')


@pytest.fixture()
def parse_recipes_expected():
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
    return expected


@pytest.fixture()
def parse_recipes_expected_json():
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
    return expected_json


@pytest.fixture()
def collect_links_expected():
    expected = {
        'Пряная дыня с глинтвейном': (
            'https://vkusvill.ru//media/recipes/pryanaya-dynya-s-glintveynom.html'
        )
    }
    return expected


@pytest.fixture()
def collect_links_expected_json():
    expected_json = json.dumps(
        {
            'Пряная дыня с глинтвейном': (
                'https://vkusvill.ru//media/recipes/pryanaya-dynya-s-glintveynom.html'
            )
        },
        indent=4,
        ensure_ascii=False
    )
    return expected_json


@pytest.fixture()
def recipes_dict_example():
    recipes_dict = Parser.collect_links(1, 2)
    return recipes_dict
