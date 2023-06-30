from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import json

def scraper(url):
    #takes the most recent URL
    #request URL while adding headers to avoid 403 Forbidden error
    req = Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/110.0')
    req.add_header('Accept', "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8")
    req.add_header("Accept-Language", "en-GB,en;q=0.5")
    req.add_header("Alt-Used", "omnivorescookbook.com")
    req.add_header("Upgrade-Insecure-Requests", "1")
    req.add_header("Sec-Fetch-Dest", "document")
    req.add_header("Sec-Fetch-Mode", "navigate")
    req.add_header("Sec-Fetch-Site", "cross-site")

    #turns this into an html_doc for BeautifulSoup to use to parse
    body = urlopen(req).read()

    #Gives us a beautiful soup object
    soup = BeautifulSoup(body, 'html.parser')

    #searching the object for a specific script tag that contains the recipe metadata
    element=soup.head.select('script[type="application/ld+json"]')[0]

    # length should be 1
    #len(element.contents)

    #pulling the text of the element as a json file
    recipe_json=element.get_text()

    #method used to parse a valid JSON string and convert it into a Python Dictionary
    new_dictionary = json.loads(recipe_json)

    #Running into a key error here sometimes -- will resolve with two paths for scraping One that continues if there is not a key error -- 

    if len(new_dictionary) == 2:
         #creates a new variable with method used to parse a valid JSON string and convert it into a Python Dictionary
        new_dictionary = json.loads(recipe_json) 
        # keysList = list(new_dictionary.keys())
        graph_dictionary = new_dictionary['@graph']
        recipe_dictionary = next((item for item in graph_dictionary if item["@type"] == "Recipe"), None)
        # new_keysList = list(recipe_dictionary.keys())

        #pulling the values of the key recipeIngredient to Display ingredients as a list
        ingredients = recipe_dictionary['recipeIngredient']     

        servings = recipe_dictionary['recipeYield']


        steps = recipe_dictionary['recipeInstructions']

        instructions = []
        for item in steps:
            if item["@type"] == "HowToStep":
                instructions.append(item['text'])

        recipe_name = recipe_dictionary['name']

        recipe_description = recipe_dictionary['description']

        return ingredients, servings, instructions, recipe_name, recipe_description
    else:
        #pulling the values of the key recipeIngredient to Display ingredients as a list
        ingredients = json.loads(recipe_json)['recipeIngredient']

        servings = json.loads(recipe_json)['recipeYield']

        instructions = json.loads(recipe_json)['recipeInstructions']

        recipe_name = json.loads(recipe_json)['name']

        recipe_description = json.loads(recipe_json)['description']

        return ingredients, servings, instructions, recipe_name, recipe_description
    
#this URL flows through the second part of the if statement -- the else statment
ingredients, servings, instructions, recipe_name, recipe_description = scraper("https://www.inspiredtaste.net/15938/easy-and-smooth-hummus-recipe")
#this URL flows through the first part of the if statment
#ingredients, servings, instructions, recipe_name, recipe_description = scraper('https://pinchofyum.com/crunchy-roll-bowls')

print(recipe_name)
print(recipe_description)
print("Ingredients:")
for i in ingredients:
    print(i)
print("Servings: ", servings)
print("Instructions:")
for i in instructions:
    print(i)

