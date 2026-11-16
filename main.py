from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig
import hashlib

from schema import get_model_config # Import the schema and prompt settings
from recipe_requests import fetch_recipe_website

load_dotenv()

# store processed recipes in a { [uuid]: [recipe] } dict
recipes = {}

# generate the recipe json data
def generate_recipe_data(url: str):
    website_contents = fetch_recipe_website(url)

    # TODO: process data with gemini
    
    return { "contents": website_contents }

# create the app, labeled using the current filename
app = Flask(__name__)

# define custom 404 page
@app.errorhandler(404)
def not_found(_):
    return render_template("404.html")

# define webpage route and callback
@app.route("/", methods=["GET"])
def homepage():
    url = request.form.get("url")
    return render_template("homepage.html", url=url)

@app.route("/generate-recipe", methods=["POST"])
def generate_recipe():
    url = request.form.get("url")

    # simply return to the home screen when no url is passed
    if not url:
        return redirect("/")

    # hash the recipe URL so we don't regenerate a recipe we've already generated
    hash = hashlib.new("sha1")
    hash.update(url.encode())
    recipe_id = hash.hexdigest()

    # check if the recipe already exists
    if not recipe_id in recipes:
        # generates the recipe from scratch if it does
        recipe = generate_recipe_data(url)

        # save the recipe for when the redirect happens
        recipes[recipe_id] = recipe

    return redirect("/recipe?id=" + recipe_id)

@app.route("/recipe", methods=["GET"])
def recipe():
    # get the id from the url search params (?id={something})
    recipe_id = request.args.get("id")

    # look up the recipe
    recipe = recipes.get(recipe_id)

    if recipe:
        return render_template("recipe.html", recipe=recipe)
    else:
        return render_template("404.html")

# Quick test of schema
@app.route("/test")  # Runs at /test
def test_schema():
    client = genai.Client()  # Reads key from .env
    response = client.models.generate_content(  # Send request to Gemini
        model="gemini-3.5-flash",  # Which Gemini model
        contents="Toast: 2 slices bread, 1 tbsp butter. 1/4 cup of peanut butter. Toast the bread, then spread with butter, and peanut butter.  Then cut into quarters.  Then smash sandwich corners on your head for 30 seconds",  # Sample recipe text
        config=get_model_config(),  # Schema and prompt setings
    )
    recipe = response.parsed  # Answer as Recipe object
    return app.response_class(recipe.model_dump_json(indent=2), mimetype="application/json")  # Pretty JSON in browser

# run the server if the file is directly executed
if __name__ == "__main__":
    app.run(debug = True)