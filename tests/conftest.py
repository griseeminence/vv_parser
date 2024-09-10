import os
import shutil

import pytest
from main import Parser
import unittest.mock as mock


@pytest.fixture(autouse=True)
def mock_request():
    with mock.patch('requests.get') as mock_request:
        # Настроим мок-объект
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