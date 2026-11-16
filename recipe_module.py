from google import genai
from google.genai.types import GenerateContentConfig
from pydantic import BaseModel
from schema import Recipe




def generate_recipe(web_html):
    with open("system_instructions.txt", "r") as file:
        instructions = file.read()

    client = genai.Client()
    response = client.models.generate_content(
        model = "gemini-3.8-flash",
        contents=web_html,
        config = GenerateContentConfig(
            system_instruction=instructions,
            response_mime_type='application/json',
            response_schema=Recipe

        )
    )

    return response.parsed