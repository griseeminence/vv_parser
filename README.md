## Parser for VV (Вкус Вилл)

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


## Modules and technologies:
### There is the main list:
(Full list in requirements.txt)

- beautifulsoup4
- lxml
- pytest
- unittest.mock
- requests
