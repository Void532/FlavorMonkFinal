"""Grocery list generation service module.

This module provides functionality to aggregate ingredient lists from multiple
meals into a single grocery list. It relies on the MealDB service to fetch
meal details and extract ingredient-measure pairs.
"""

from typing import List, Dict

from .meal_db import lookup_meal_by_id


def extract_ingredients_from_meal(meal_data: dict) -> Dict[str, str]:
    """Extract ingredients and measures from a meal record.

    TheMealDB API returns up to 20 ingredient and measure pairs in
    fields strIngredient1..strIngredient20 and strMeasure1..strMeasure20.
    This function iterates through these fields and returns a dictionary
    mapping ingredient names to their respective measures.

    Args:
        meal_data: A dictionary representing a single meal record from
            TheMealDB API.

    Returns:
        A dictionary mapping ingredient names to measure strings.
    """
    ingredients: Dict[str, str] = {}
    for i in range(1, 21):
        ing_key = f"strIngredient{i}"
        measure_key = f"strMeasure{i}"
        ingredient = meal_data.get(ing_key)
        measure = meal_data.get(measure_key)
        if ingredient and ingredient.strip():
            # Normalize ingredient and measure strings
            name = ingredient.strip()
            qty = measure.strip() if measure else ""
            ingredients[name] = qty
    return ingredients


def create_grocery_list(meal_ids: List[int]) -> Dict[str, str]:
    """Aggregate ingredients across multiple meals into a grocery list.

    Given a list of MealDB meal IDs, this function looks up each meal,
    extracts its ingredient list and measures, then combines them into
    a single grocery list. If an ingredient appears in multiple meals,
    the measures are concatenated as a comma-separated string. This
    simplistic aggregation leaves precise quantity calculations to
    future improvements, but it provides a consolidated view of
    required ingredients.

    Args:
        meal_ids: A list of integers representing MealDB meal identifiers.

    Returns:
        A dictionary mapping ingredient names to aggregated measure strings.
    """
    grocery: Dict[str, str] = {}
    for meal_id in meal_ids:
        meal_response = lookup_meal_by_id(meal_id)
        meals = meal_response.get("meals") if isinstance(meal_response, dict) else None
        if not meals:
            continue
        meal_data = meals[0]
        ingredients = extract_ingredients_from_meal(meal_data)
        for ingredient, measure in ingredients.items():
            if ingredient in grocery:
                # Append measure if provided
                if measure:
                    if grocery[ingredient]:
                        grocery[ingredient] += f", {measure}"
                    else:
                        grocery[ingredient] = measure
            else:
                grocery[ingredient] = measure
    return grocery
