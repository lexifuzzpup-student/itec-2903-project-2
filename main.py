from flask import Flask, render_template, request, send_from_directory
from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig

from schema import get_model_config # Import the schema and prompt settings

load_dotenv()

# create the app, labeled using the current filename
app = Flask(__name__)

# define webpage route and callback
@app.route("/")
def homepage():
    return 'hello!'

# Quick test of schema
@app.route("/test")  # Runs at /test
def test_schema():
    client = genai.Client()  # Reads key from .env
    response = client.models.generate_content(  # Send request to Gemini
        model="gemini-3.5-flash",  # Which Gemini model
        contents="Toast: 2 slices bread, 1 tbsp butter. 1/4 cup of peanut butter. Toast the bread, then spread with butter, and peanut butter.  Then cut into quarters.  Then smash sandwich corners on your head",  # Sample recipe text
        config=get_model_config(),  # Schema and prompt setings
    )
    recipe = response.parsed  # Answer as Recipe object
    return app.response_class(recipe.model_dump_json(indent=2), mimetype="application/json")  # Pretty JSON in browser

# run the server if the file is directly executed
if __name__ == "__main__":
    app.run(debug = True)