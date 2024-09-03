import os

from bs4 import BeautifulSoup
import requests
import json
import time
import random

headers2 = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

# url = "https://vkusvill.ru/media/recipes/"
# req = requests.get(url, headers=headers)
# src = req.text

# with open(f'data/first_page.html', "w", encoding='utf-8') as file:
#     file.write(src)

with open("data/first_page.html", encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")
recipes_links = soup.find_all(class_='VV_NewsCard__Layout')

recipes_dict = {}

for i in recipes_links:
    i_text = i.get('aria-label').replace('\xa0', ' ')
    i_href = i.get('href')
    recipes_dict[i_text] = 'https://vkusvill.ru/' + i_href

for i,y in recipes_dict.items():
    print(y)

# Список активных ссылок на рецепты с первой страницы
full_links = [('https://vkusvill.ru/' + link) for link in recipes_dict.values()]

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
print(recipes_dict)
full_links2 =['https://vkusvill.ru/media/recipes/pryanaya-dynya-s-glintveynom.html']
result = []
for title, link in recipes_dict.items():
    req = requests.get(link, headers=headers)


    with open(f"data/recipe_{title.replace(' ', '_')}.html", "w", encoding='utf-8') as file:
        file.write(req.text)

    with open(f"data/recipe_{title.replace(' ', '_')}.html", encoding='utf-8') as file:
        src = file.read()



    print(link)
    print(title)
    recipe_number = 1
    # Сохранение HTML в переменную вместо записи в файл
    # src2 = req.text

    # Парсинг HTML с BeautifulSoup
    soup = BeautifulSoup(src, "lxml")
    title = soup.find('title')
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
    dict_element = {title.text: {"Steps": steps_strip, "Ingredients": ingredients_dict}}
    # print(dict_element)
    # with open("data/recipe_data.json", "a", encoding="utf-8") as file:
    #     json.dump(dict_element, file, indent=4, ensure_ascii=False)
    result.append(dict_element)
    time.sleep(random.randrange(3, 6))
    print(f'Рецепт {recipe_number} обработан')
    recipe_number += 1


with open("data/result_data.json", "a", encoding="utf-8") as file:
    json.dump(result, file, indent=4, ensure_ascii=False)