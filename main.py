from flask import Flask, render_template, request, send_from_directory
from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig
from recipe_module import generate_recipe


from recipe_requests import fetch_recipe_website

load_dotenv()

# create the app, labeled using the current filename
app = Flask(__name__)

# define webpage route and callback
@app.route("/",methods=["GET","POST"])
def homepage():
    url = request.form.get("url")
    return render_template("homepage.html",url=url)

@app.route("/result",methods=["GET","POST"])
def result():
    url = request.form.get("url")
    web_html = fetch_recipe_website(url)
    recipe =  generate_recipe(web_html)
    return render_template("result.html",recipe=recipe)

# run the server if the file is directly executed
if __name__ == "__main__":
    app.run(debug = True)