from google import genai
from google.genai.types import GenerateContentConfig

with open("system_instructions.txt", "r") as file:
    instructions = file.read()
# Create html function to go ito contents

client = genai.Client()
response = client.models.generate_content(
    model = "gemini-3.8-flash",
    contents = """
    """,
    config = GenerateContentConfig(
        system_instruction=instructions,

    )
)