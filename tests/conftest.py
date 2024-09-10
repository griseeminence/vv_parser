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
            '<a href="/media/recipes/pryanaya-dynya-s-glintveynom.html" '
            'data-news-id="5584103" class="VV_NewsCard__Layout" '
            'aria-label="Пряная дыня с&nbsp;глинтвейном"></a>'
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