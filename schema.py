# Recipe schema for Gemini
from __future__ import annotations

from google.genai.types import GenerateContentConfig  # Gemini's model config class
from pydantic import BaseModel  # Pydantic builds the schema


# One ingredient going into a step
class IngredientUse(BaseModel):
    id: str  # Points to an Ingredient
    amount: str | None  # Split portion, or null


# One line of the ingredient list
class Ingredient(BaseModel):
    id: str  # Uniqe id like i1
    quantity: float | None  # Number like 1.5
    unit: str | None  # Cup, tbsp, or null
    name: str  # Ingredient name only
    prep: str | None  # Prep note if any


# One step in the directions
class Step(BaseModel):
    id: str  # Step id like s1
    order: int  # Positon in the directions
    short: str  # Label for grid cells
    text: str  # Shown in traditional view
    duration_min: float | None  # Minutes, or null
    uses_ingredients: list[IngredientUse]  # Ingredients joining this step


# The whole recipe, top levle
class Recipe(BaseModel):
    title: str | None  # The recipe's name
    description: str | None  # Short summary from source
    prep_time_min: int | None  # Prep time in minutes
    cook_time_min: int | None  # Cook time in minutes
    total_time_min: int | None  # Totel time in minutes
    servings: int | None  # How many it serves
    ingredients: list[Ingredient]  # Full ingredient list
    steps: list[Step]  # Directions in order
    notes: list[str]  # Cook's tips, if any

