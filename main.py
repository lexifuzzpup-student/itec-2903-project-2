from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig
from uuid import uuid4

from recipe_requests import fetch_recipe_website

load_dotenv()

# store processed recipes in a { [uuid]: [recipe] } dict
recipes = {}

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
    recipe = { "ingredients": [ "lots of love" ] }
    recipe_id = str(uuid4())

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

# run the server if the file is directly executed
if __name__ == "__main__":
    app.run(debug = True)