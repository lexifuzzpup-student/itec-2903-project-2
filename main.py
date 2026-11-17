from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
from google import genai
from google.genai import errors as genai_errors
from requests import RequestException
import hashlib
import os

import recipe_module

load_dotenv()
client = genai.Client()                 # Reads key from .env
model = os.environ["GEMINI_MODEL"]      # Reads from .env - If this throws, add it to your environment variables (see .env.example)

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
        try:
            recipe = recipe_module.generate_recipe(client, model, url)
        except RequestException:
            return render_template("error.html", errors = [
                "Failed to fetch website data. Check if your URL is formatted correctly and the website is responding, and try again."
            ]), 400
        except genai_errors.APIError as error:
            print(error)
            return render_template("error.html", errors = [
                "Something went wrong while summarizing. Try again in a few minutes.",
                error.message
            ]), 500

        if not recipe:
            return render_template("error.html", errors = [
                "No recipe was generated. Please try again."
            ]), 500
        if recipe.error:
            return render_template("error.html", errors = [
                recipe.error
            ]), 500

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