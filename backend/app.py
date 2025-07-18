from fastapi import FastAPI
from .routers import recipes

from typing import List

app = FastAPI(title="FlavorMonk API", description="Backend for FlavorMonk meal planning app")
# Include recipe routes
app.include_router(recipes.router)


@app.get("/")
def read_root():
    # Incde_router(recipes.router) (moved above)

    """Root endpoint returns a welcome message."""
    return {"message": "Welcome to FlavorMonk API"}

@app.get("/health")
def health() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}

@app.get("/recipes/search")
def search_recipes(query: str) -> dict:
    """Placeholder endpoint for searching recipes.

    In a production environment this function would query TheMealDB API
    or another recipe database using the provided query string and return
    structured recipe data.
    """
    # TODO: Integrate with TheMealDB or other recipe API
    return {"query": query, "results": []}

@app.post("/grocery-list")
def generate_grocery_list(meals: List[str]) -> dict:
    """Placeholder endpoint for generating a grocery list from meal names.

    Parameters:
        meals: A list of meal identifiers or names.

    Returns:
        A dictionary containing a draft shopping list. In production this
        would aggregate ingredients across recipes, adjust quantities and
        incorporate expiration and pricing data.
    """
    # TODO: Implement grocery optimization logic
    return {"grocery_list": []}
