# VV Parser (Вкус Вилл)

This project is a Python-based web scraper that collects recipe information
from the VkusVill website. The parser retrieves links to recipes, downloads
the corresponding HTML pages, and extracts recipe details, including ingredients
and preparation steps. The results are saved in JSON format for easy access and
further analysis.

## About:
1. It gathers information from pages featuring healthy recipes, including HTML
pages and a collection of specific recipe links.
2. It saves the HTML pages in a designated data directory and also generates a
JSON file with a dictionary of "Recipe Name: Link".
3. It retrieves information from specific recipes (using the dictionary with
links).
4. It stores the HTML pages in a dedicated data directory and also creates a
JSON file containing a list of dictionaries with titles, ingredients, and
cooking steps.

* There are pytest tests included for basic usability checks.
* Additional information is displayed in the console to indicate
the progress of data collection.
* A logger is implemented to capture details about the parsing process.
* A delay of several seconds is added before each request to prevent
being blocked.

## Requirements

- Python 3.x
- `requests` library for handling HTTP requests
- `BeautifulSoup` from `bs4` for parsing HTML content
- `lxml` for XML parsing (optional, but recommended for better performance)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
    ```
2. Install the required libraries:
   ```
    pip install -r requirements.txt
    ```

# Usage
1. Open the parser.py file in your favorite text editor or IDE.
2. Run the script from the command line:
    ```
    python parser.py
    ```
3. Follow the prompts to specify the range of pages you want to parse:
    ```
    Specify the starting page for parsing:
    Specify the ending page for parsing:
    ```
4. The parser will collect links to the recipes, download the corresponding HTML pages
and extract recipe details. The output will be saved in the data/ directory.
   - Collected recipe links will be saved in data/recipe_pages/result_recipe_pages.json.
   - Recipe details will be saved in data/result_data.json.

5. Directory Structure
    ```
    .
    ├── data/
    │   ├── recipe_pages/
    │   │   └── result_recipe_pages.json
    │   │   └── page_1.html
    │   │   └── page_2.html
    │   │   └── ...
    │   └── result_data.json
    ├── parser.py
    └── README.md
    ```

# Contributing
- Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

# License
- This project is licensed under the MIT License.