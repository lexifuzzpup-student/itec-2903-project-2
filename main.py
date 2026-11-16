from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
from google import genai
import hashlib

import recipe_module

load_dotenv()
client = genai.Client()  # Reads key from .env

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
        recipe = recipe_module.generate_recipe(client, url)

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