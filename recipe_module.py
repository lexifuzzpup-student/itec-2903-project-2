from google import genai
from google.genai.types import GenerateContentConfig
from recipe_requests import fetch_recipe_website

with open("system_instructions.txt", "r") as file:
    instructions = file.read()
url = input("Enter recipe URL: ").strip()
website_html = fetch_recipe_website(url)

client = genai.Client()
response = client.models.generate_content(
    model = "gemini-3.8-flash",
    contents=website_html,
    config = GenerateContentConfig(
        system_instruction=instructions,

    )
)
print(response.text)