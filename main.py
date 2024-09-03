import os

import requests
import json
import time
import random
from bs4 import BeautifulSoup

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}


PAGE_NUMBER = 66


def collect_links(start_page, end_page):
    recipes_dict = {}
    page_counter = start_page
    print(f'Принято страниц на обработку: {end_page - start_page}')

    for page in range(start_page, end_page):

        url_pages = f'https://vkusvill.ru/media/recipes/?utm_source=site&utm_medium=main&utm_campaign=content&PAGEN_1={page}'
        req = requests.get(url_pages, headers=headers)
        folder_name = f"data/recipe_pages/"

        if os.path.exists(folder_name):
            print("Папка для сохранения файлов уже существует. Продолжаю парсить!")
        else:
            os.mkdir(folder_name)

        with open(f'data/recipe_pages/page_{page}.html', 'w', encoding='utf-8') as file:
            file.write(req.text)
        with open(f'data/recipe_pages/page_{page}.html', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        recipes_links = soup.find_all(class_='VV_NewsCard__Layout')

        for i in recipes_links:
            i_text = i.get('aria-label').replace('\xa0', ' ')
            i_href = i.get('href')
            recipes_dict[i_text] = 'https://vkusvill.ru/' + i_href

        print(f'Страница {page_counter} обработана!')
        page_counter += 1
        time.sleep(random.randrange(2, 4))

    with open("data/recipe_pages/result_recipe_pages.json", "a", encoding="utf-8") as file:
        json.dump(recipes_dict, file, indent=4, ensure_ascii=False)
        print(f'JSON со списком всех ссылок сохранён!')
    return parse_recipes(recipes_dict)

# Список активных ссылок на рецепты с первой страницы
# full_links = [('https://vkusvill.ru/' + link) for link in recipes_dict.values()]

# for i in recipes_dict.values():
#     full_links.append('https://vkusvill.ru/'+i)

# print(full_links)
# print(recipes_dict.keys())

# Парсим страницу с отдельным рецептом
# url = "https://vkusvill.ru//media/recipes/pryanaya-dynya-s-glintveynom.html"
# req = requests.get(url, headers=headers)
# src = req.text

# with open(f'data/first_recipe.html', encoding='utf-8') as file:
#     src = file.read()
# print(recipes_dict)

# Для теста
# full_links2 = ['https://vkusvill.ru/media/recipes/pryanaya-dynya-s-glintveynom.html']


result = []


def parse_recipes(recipes_dict):
    recipe_number = 1
    print(f'Количество собранных рецептов: {len(recipes_dict)}')
    for title, link in recipes_dict.items():
        req = requests.get(link, headers=headers)

        folder_name = f"data/recipes/"

        if not os.path.exists(folder_name):
            os.mkdir(folder_name)

        with open(f'{folder_name}_{title.replace(" ", "_")}.html', 'w', encoding='utf-8') as file:
            file.write(req.text)

        with open(f'{folder_name}_{title.replace(" ", "_")}.html', encoding='utf-8') as file:
            src = file.read()


        # Сохранение HTML в переменную вместо записи в файл
        # src2 = req.text

        # Парсинг HTML с BeautifulSoup
        soup = BeautifulSoup(src, "lxml")
        # title = soup.find('title')
        ingredients_name_list = soup.find_all(class_='VV_RecipeDetailIng__Col _name')
        ingredients_value_list = soup.find_all(class_='VV_RecipeDetailIng__Col _val b500')
        ingredients_name_strip = [ingredient.text.strip() for ingredient in ingredients_name_list]
        ingredients_value_strip = [ingredient.text.strip() for ingredient in ingredients_value_list]
        ingredients_dict = dict(zip(ingredients_name_strip, ingredients_value_strip))

        # print(ingredients_name_strip)
        # print(ingredients_value_strip)
        steps_list = soup.find_all(class_='VV_RecipeDetailSteps__StepSubtitle body_article')
        steps_strip = [step.text.strip().replace('\xa0', ' ') for step in steps_list]

        # print(steps_strip)
        # print(ingredients_dict)
        # Результирующий словарь, собирающий со страницы рецепта название, шаги и ингредиенты
        dict_element = {title: {"Steps": steps_strip, "Ingredients": ingredients_dict}}
        # print(dict_element)
        # with open("data/recipe_data.json", "a", encoding="utf-8") as file:
        #     json.dump(dict_element, file, indent=4, ensure_ascii=False)
        result.append(dict_element)
        time.sleep(random.randrange(3, 6))
        print(f'Рецепт {recipe_number} обработан')
        recipe_number += 1

    with open("data/result_data.json", "a", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    collect_links(1,3)