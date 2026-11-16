# Recipe schema for Gemini
from google.genai.types import GenerateContentConfig  # Gemini's model config class
from pydantic import BaseModel  # Pydantic builds the schema


# One line of the ingredient list
class Ingredient(BaseModel):
    quantity: float | None  # Number like 1.5
    unit: str | None  # Cup, tbsp, or null
    name: str  # Ingredeint name only
    prep: str | None  # Prep note if any


# One step in the directions
class Step(BaseModel):
    text: str  # Full instruction text
    duration_min: float | None  # Minutes, or null


# The whole recipe, top levle
class Recipe(BaseModel):
    is_recipe: bool  # False if not recipe
    error: str | None  # Reason it failed
    title: str | None  # The recipe's name
    description: str | None  # Short summary from source
    prep_time_min: float | None  # Prep time in minutes
    cook_time_min: float | None  # Cook time in minutes
    total_time_min: float | None  # Totel time in minutes
    servings: str | None  # As written, like "4-6"
    ingredients: list[Ingredient]  # Full ingredient list
    steps: list[Step]  # Directions in order
    notes: list[str]  # Cook's tips


