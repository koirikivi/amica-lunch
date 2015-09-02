from __future__ import print_function, unicode_literals, absolute_import
from datetime import datetime
import sys
import requests
import re
try:
    input = raw_input
except NameError:
    pass

MENU_URL = "http://www.amica.fi/api/restaurant/menu/day?date={date}&language=en&restaurantPageId={restaurant_id}"
RECIPE_URL = "http://www.amica.fi/api/restaurant/menu/recipe?language=en&recipeId={recipe_id}"
RESTAURANT_IDS = {
    "smarthouse": 8754,
}
#per 100g: 91 kcal, 381 kJ, 2,0 g Fat incl, 0,7 g saturates, 16,2 g CHO incl, 0,7 g sugars, 1,8 g Protein, 0,3 g Salt
NUTRIENTS_REGEX = re.compile(
    r'per (?P<serving>\d+.*?): (?P<kcal>\d*\s?\d+) kcal, (?P<kj>\d*\s?\d+) kJ, '
    r'(?P<fat>\d+,\d+) g Fat incl, (?P<saturates>\d+,\d+) g saturates, '
    r'(?P<carbohydrates>\d+,\d+) g CHO incl, (?P<sugars>\d+,\d+) g sugars, '
    '(?P<protein>\d+,\d+) g Protein, '
    r'(?P<salt>\d+,\d+) g Salt'
, re.UNICODE)

def get_test_lunch():
    import os, json
    filename = "menu-2015-09-02.json"
    with open(os.path.join(os.path.dirname(__file__), filename), "r") as f:
        return json.load(f)["LunchMenu"]

def get_lunch(date, restaurant_id):
    if hasattr(date, "date"):
        date = date.date()  # convert from datetime to date
    if not isinstance(date, basestring):
        date = date.isoformat()
    response = requests.get(MENU_URL.format(date=date, restaurant_id=restaurant_id))
    assert response.status_code == 200
    return response.json()["LunchMenu"]

def get_recipe(recipe_id):
    response = requests.get(RECIPE_URL.format(recipe_id=recipe_id))
    assert response.status_code == 200
    return response.json()

def parse_nutrients(recipe):
    ingredients_str = recipe["Ingredients"]
    nutrients_str = ingredients_str.split("\n")[1].strip()
    match = re.match(NUTRIENTS_REGEX, nutrients_str)
    if match:
        return match.groupdict()
    else:
        return {}

def print_lunch(lunch):
    print("Lunch options for {} {}".format(lunch["DayOfWeek"], lunch["Date"]))
    for menu in lunch["SetMenus"]:
        print(menu["Name"])
        for meal in menu["Meals"]:
            print("   {}".format(meal["Name"]))

def ask_menu(lunch):
    menu_index = input("Get nutrients by entering index of menu (1-based): ")
    try:
        menu_index = int(menu_index)
        menu = lunch["SetMenus"][menu_index - 1]
        return menu
    except (IndexError, ValueError):
        print("Invalid input!")
        return None

def print_menu_nutrients(menu):
    print(menu["Name"])
    format_str = "{name:50} {serving:>14} {kcal:>8} {protein:>8} {fat:>8} {carbohydrates:>8}"
    print(format_str.format(name="meal", serving="serv", kcal="kcal",
                            protein="prot", fat="fat", carbohydrates="carbs"))
    for meal in menu["Meals"]:
        recipe = get_recipe(meal["RecipeId"])
        nutrients = parse_nutrients(recipe)
        print(format_str.format(name=meal["Name"], **nutrients))

def run_cli():
    restaurant_id = RESTAURANT_IDS["smarthouse"]
    lunch = get_lunch(datetime.now(), restaurant_id)
    print_lunch(lunch)
    while True:
        menu = ask_menu(lunch)
        if menu:
            print_menu_nutrients(menu)

if __name__ == "__main__":
    run_cli()
