from fastapi import APIRouter
from app.api.endpoints import snippets

api_router = APIRouter()

# Include the snippets endpoints
api_router.include_router(snippets.router, tags=["snippets"])