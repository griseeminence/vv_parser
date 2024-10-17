import json
import os
import requests
import random
import time

from bs4 import BeautifulSoup

# Define headers for the HTTP requests to mimic a real browser
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}


class Parser:
    @staticmethod
    def collect_links(start_page=1, end_page=66):
        """
        Collects recipe links from the specified range of pages.

        Args:
            start_page (int): The starting page number.
            end_page (int): The ending page number.

        Returns:
            dict: A dictionary containing recipe titles and their corresponding URLs.
        """
        # Create a directory for storing data if it doesn't exist
        if not os.path.exists('data/'):
            os.mkdir('data/')
        recipes_dict = {}  # Dictionary to store recipe titles and links
        page_counter = start_page
        print(f'Pages to process: {end_page - start_page}')

        # Loop through the specified range of pages
        for page in range(start_page, end_page):
            url_pages = f'https://vkusvill.ru/media/recipes/?utm_source=site&utm_medium=main&utm_campaign=content&PAGEN_1={page}'
            try:
                req = requests.get(url_pages, headers=headers)
                req.raise_for_status()
            except requests.RequestException as e:
                print(f"Error requesting page #{page}: {e}")
                continue

            # Create a directory for recipe pages if it doesn't exist
            folder_name = f'data/recipe_pages/'
            if not os.path.exists(folder_name):
                os.mkdir(folder_name)

            # Save and read the HTML of the page
            with open(f'data/recipe_pages/page_{page}.html', 'w', encoding='utf-8') as file:
                file.write(req.text)
            with open(f'data/recipe_pages/page_{page}.html', encoding='utf-8') as file:
                src = file.read()

            # Parse the HTML with BeautifulSoup
            soup = BeautifulSoup(src, "lxml")
            recipes_links = soup.find_all(class_='VV_NewsCard__Layout')

            # Collect recipe titles and links
            for i in recipes_links:
                i_text = i.get('aria-label').replace('\xa0', ' ')
                i_href = i.get('href')
                recipes_dict[i_text] = 'https://vkusvill.ru/' + i_href

            print(f'Processed page {page_counter}!')
            page_counter += 1
            time.sleep(random.randrange(2, 4))  # Sleep to prevent overwhelming the server

        # Save the collected links to a JSON file
        with open("data/recipe_pages/result_recipe_pages.json", "a", encoding="utf-8") as file:
            json.dump(recipes_dict, file, indent=4, ensure_ascii=False)
            print('JSON with all links saved!')

        return recipes_dict

    @staticmethod
    def parse_recipes(recipes_dict):
        """
        Parses the details of each recipe from the collected links.

        Args:
            recipes_dict (dict): A dictionary containing recipe titles and their corresponding URLs.

        Returns:
            list: A list of dictionaries containing recipe details (ingredients and steps).
        """
        result = []  # List to store recipe details
        recipe_number = 1
        print(f'Total collected recipes: {len(recipes_dict)}')

        # Loop through each recipe link to extract details
        for title, link in recipes_dict.items():
            try:
                req = requests.get(link, headers=headers)
                req.raise_for_status()
            except requests.RequestException as e:
                print(f"Error requesting {link}: {e}")
                continue

            # Create a directory for recipe details if it doesn't exist
            folder_name = f'data/recipes/'
            if not os.path.exists(folder_name):
                os.mkdir(folder_name)

            # Save and read the HTML of the recipe page
            with open(f'{folder_name}_{title.replace(" ", "_")}.html', 'w', encoding='utf-8') as file:
                file.write(req.text)
            with open(f'{folder_name}_{title.replace(" ", "_")}.html', encoding='utf-8') as file:
                src = file.read()

            # Parse the recipe details with BeautifulSoup
            soup = BeautifulSoup(src, "lxml")
            ingredients_name_list = soup.find_all(class_='VV_RecipeDetailIng__Col _name')
            ingredients_value_list = soup.find_all(class_='VV_RecipeDetailIng__Col _val b500')

            # Create a dictionary of ingredients
            ingredients_dict = dict(zip(
                [i.text.strip() for i in ingredients_name_list],
                [i.text.strip() for i in ingredients_value_list]
            ))

            # Extract recipe steps
            steps_list = soup.find_all(class_='VV_RecipeDetailSteps__StepSubtitle body_article')
            steps_strip = [step.text.strip().replace('\xa0', ' ') for step in steps_list]

            # Store the recipe details in a dictionary
            dict_element = {title: {"Steps": steps_strip, "Ingredients": ingredients_dict}}
            result.append(dict_element)
            time.sleep(random.randrange(2, 4))  # Sleep to prevent overwhelming the server
            print(f'Recipe #{recipe_number} ({title}) processed!')

            recipe_number += 1

        # Save the recipe details to a JSON file
        with open("data/result_data.json", "a", encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
            print('JSON with recipe data saved!')

        return result

    @staticmethod
    def start_parser(start, end):
        """
        Initiates the parsing process.

        Args:
            start (int): The starting page number.
            end (int): The ending page number.

        Returns:
            list: A list of dictionaries containing recipe details.
        """
        recipes_dict = Parser.collect_links(start, end)  # Collect recipe links
        return Parser.parse_recipes(recipes_dict)  # Parse the collected recipes


# Entry point of the script
if __name__ == "__main__":
    page_start = int(input('Specify the starting page for parsing:\n'))
    page_end = int(input('Specify the ending page for parsing:\n\n'))
    Parser.start_parser(page_start, page_end)  # Start the parsing process
