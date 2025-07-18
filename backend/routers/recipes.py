"""
API router for recipe-related endpoints.

These endpoints interface with the TheMealDB service layer to fetch and filter recipes.
They provide a thin layer over the service functions and handle HTTP errors gracefully.
"""
from fastapi import APIRouter, HTTPException
from typing import Any
from ..services import meal_db

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get("/search")
def search_recipes(name: str) -> Any:
    """Search for recipes by name.

    Args:
        name: The name or partial name of the recipe to search for.

    Returns:
        A JSON object containing search results from TheMealDB.
    """
    try:
        return meal_db.search_meal_by_name(name)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/{meal_id}")
def get_recipe(meal_id: int) -> Any:
    """Retrieve detailed information about a single recipe by ID.

    Args:
        meal_id: TheMealDB unique meal identifier.

    Returns:
        A JSON object with detailed meal information.
    """
    try:
        return meal_db.lookup_meal_by_id(meal_id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/by_ingredient")
def filter_by_ingredient(ingredient: str) -> Any:
    """Filter recipes by a specific ingredient.

    Args:
        ingredient: Ingredient to filter meals by.

    Returns:
        A JSON object with meals containing the ingredient.
    """
    try:
        return meal_db.filter_meals_by_ingredient(ingredient)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
