from fastapi import FastAPI
from .routers import recipes, grocery

app = FastAPI(
    title="FlavorMonk API",
    description="Backend for FlavorMonk meal planning app"
)

# Include routers
app.include_router(recipes.router)
app.include_router(grocery.router)

@app.get("/")
def read_root():
    """Root endpoint returns a welcome message."""
    return {"message": "Welcome to FlavorMonk API"}

@app.get("/health")
def health() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}
