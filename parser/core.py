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


class Parser:
    @staticmethod
    def collect_links(start_page=1, end_page=66):
        if not os.path.exists('data/'):
            os.mkdir('data/')
        recipes_dict = {}
        page_counter = start_page
        print(f'Принято страниц на обработку: {end_page - start_page}')

        for page in range(start_page, end_page):
            url_pages = f'https://vkusvill.ru/media/recipes/?utm_source=site&utm_medium=main&utm_campaign=content&PAGEN_1={page}'
            try:
                req = requests.get(url_pages, headers=headers)
                req.raise_for_status()
            except requests.RequestException as e:
                print(f"Ошибка при запросе страницы № {page}: {e}")
                continue

            folder_name = f'data/recipe_pages/'
            if not os.path.exists(folder_name):
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

        return recipes_dict

    @staticmethod
    def parse_recipes(recipes_dict):
        result = []
        recipe_number = 1
        print(f'Количество собранных рецептов: {len(recipes_dict)}')

        for title, link in recipes_dict.items():
            try:
                req = requests.get(link, headers=headers)
                req.raise_for_status()
            except requests.RequestException as e:
                print(f"Ошибка при запросе {link}: {e}")
                continue
            folder_name = f'data/recipes/'
            if not os.path.exists(folder_name):
                os.mkdir(folder_name)

            with open(f'{folder_name}_{title.replace(" ", "_")}.html', 'w', encoding='utf-8') as file:
                file.write(req.text)
            with open(f'{folder_name}_{title.replace(" ", "_")}.html', encoding='utf-8') as file:
                src = file.read()

            soup = BeautifulSoup(src, "lxml")
            ingredients_name_list = soup.find_all(class_='VV_RecipeDetailIng__Col _name')
            ingredients_value_list = soup.find_all(class_='VV_RecipeDetailIng__Col _val b500')
            ingredients_dict = dict(zip(
                [i.text.strip() for i in ingredients_name_list],
                [i.text.strip() for i in ingredients_value_list]
            ))
            steps_list = soup.find_all(class_='VV_RecipeDetailSteps__StepSubtitle body_article')
            steps_strip = [step.text.strip().replace('\xa0', ' ') for step in steps_list]
            dict_element = {title: {"Steps": steps_strip, "Ingredients": ingredients_dict}}
            result.append(dict_element)
            time.sleep(random.randrange(2, 4))
            print(f'Рецепт №{recipe_number} ({title}) обработан!')

            recipe_number += 1

        with open("data/result_data.json", "a", encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
            print(f'JSON с данными о рецептах сохранён!')

        return result

    @staticmethod
    def start_parser(start, end):
        recipes_dict = Parser.collect_links(start, end)
        return Parser.parse_recipes(recipes_dict)


if __name__ == "__main__":
    page_start = int(input('Укажите начальную страницу для парсинга:\n'))
    page_end = int(input('Укажите конечную страницу для парсинга:\n'))
    Parser.start_parser(page_start, page_end)
