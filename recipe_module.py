from google import genai
from google.genai.types import GenerateContentConfig
from recipe_requests import fetch_recipe_website
from schema import Recipe

# Model config holds the schema and system instructions
def get_model_config():
    with open("system_instructions.txt", "r") as file:
        instructions = file.read()

    return GenerateContentConfig(
        system_instruction=instructions,  # Gemini's ground rulles
        response_mime_type="application/json",  # Reply in JSON only
        response_schema=Recipe,  # Classes become the schema
    )

# generate the recipe json data
def generate_recipe(client: genai.Client, url: str):
    website_html = fetch_recipe_website(url)
    
    # Send request to Gemini
    response = client.models.generate_content(
        model="gemini-3.8-flash",   # Which Gemini model
        contents=website_html,      # Website HTML is the input prompt
        config=get_model_config(),  # Schema and prompt setings
    )

    # get the parsed json that gemini created
    recipe = response.parsed
    
    return recipe