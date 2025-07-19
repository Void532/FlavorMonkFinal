"""API router for generating grocery lists.

This router defines an endpoint that accepts a list of meal IDs and
returns a consolidated grocery list generated from the associated
recipes. It uses the service layer to aggregate ingredient quantities
and handles basic error reporting.
"""

from typing import List, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..services.grocery import create_grocery_list


class GroceryRequest(BaseModel):
    """Request model for generating a grocery list.

    Attributes:
        meal_ids: A list of MealDB meal identifiers for which to
            generate the grocery list.
    """
    meal_ids: List[int]


router = APIRouter()


@router.post("/grocery", response_model=Dict[str, Dict[str, str]])
def generate_grocery_list(request: GroceryRequest) -> Dict[str, Dict[str, str]]:
    """Generate a grocery list for the given meal IDs.

    This endpoint calls the grocery service to aggregate ingredients
    across all specified meals. If successful, it returns a dictionary
    containing a single key ``grocery_list`` whose value is another
    dictionary mapping ingredient names to aggregated measures.

    Args:
        request: A ``GroceryRequest`` object containing a list of meal IDs.

    Returns:
        A dictionary with one key ``grocery_list`` mapping to the
        aggregated grocery list.

    Raises:
        HTTPException: If an error occurs during list generation.
    """
    try:
        grocery = create_grocery_list(request.meal_ids)
        return {"grocery_list": grocery}
    except Exception as exc:
        # Bubble up exception details in a controlled manner
        raise HTTPException(status_code=500, detail=str(exc))
