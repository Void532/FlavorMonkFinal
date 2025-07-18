"""
Service module for interacting with TheMealDB API.

This module provides simple wrapper functions around TheMealDB endpoints.
It can be extended to include caching, authentication (for premium access) and
error handling. In production, consider adding retries, timeouts and logging.
"""
import os
from typing import Any, Dict

import requests

# Base URL for the public TheMealDB API (free tier). For premium access,
# the base URL or authentication parameters may need to be updated.
BASE_URL = "https://www.themealdb.com/api/json/v1/1"


def _get(endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Internal helper to perform a GET request and return JSON.

    Args:
        endpoint: API path after the base URL.
        params: Query parameters to include in the request.

    Returns:
        Parsed JSON response as a dictionary.

    Raises:
        requests.HTTPError: If the HTTP request returned an unsuccessful status code.
    """
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def search_meal_by_name(name: str) -> Dict[str, Any]:
    """Search meals by name.

    Args:
        name: Name or partial name of the meal.

    Returns:
        JSON response containing meal details if found.
    """
    return _get("search.php", {"s": name})


def lookup_meal_by_id(meal_id: int) -> Dict[str, Any]:
    """Lookup a meal by its unique ID.

    Args:
        meal_id: Unique identifier for the meal.

    Returns:
        JSON response containing details for the specified meal.
    """
    return _get("lookup.php", {"i": meal_id})


def filter_meals_by_ingredient(ingredient: str) -> Dict[str, Any]:
    """Filter meals by a specific ingredient.

    Args:
        ingredient: Ingredient name to filter meals.

    Returns:
        JSON response containing meals that include the given ingredient.
    """
    return _get("filter.php", {"i": ingredient})
