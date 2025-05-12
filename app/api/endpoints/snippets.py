from fastapi import APIRouter, Depends, Query
from datetime import date as date_type
import datetime
from typing import Optional, List

from app.schemas.snippet import SnippetRequest, SnippetResponse, SnippetsResponse
from app.services.snippet_service import get_snippets

router = APIRouter()

@router.get("/snippets", response_model=SnippetsResponse, summary="Get snippets by filters")
async def get_snippets_endpoint(
    team_name: Optional[str] = Query(None, description="Team name or alias"),
    date_from: Optional[str] = Query(None, description="Start date in YYYY-MM-DD format"),
    date_to: Optional[str] = Query(None, description="End date in YYYY-MM-DD format"),
    user_name: Optional[str] = Query(None, description="User name to filter by")
):
    """
    Get snippets based on the provided filters:
    
    - **team_name**: Team name or alias (optional)
    - **date_from**: Start date in YYYY-MM-DD format (optional, defaults to 2000-01-01)
    - **date_to**: End date in YYYY-MM-DD format (optional, defaults to today)
    - **user_name**: User name to filter by (optional)
    
    Returns an array of snippets matching the criteria
    """
    # Set default dates if not provided
    if date_from is None:
        date_from = "2000-01-01"
    
    # Set today's date as default for date_to if not provided
    if date_to is None:
        date_to = datetime.date.today().strftime("%Y-%m-%d")
    
    # Call service function to get snippets
    snippets = get_snippets(
        team_name=team_name,
        date_from=date_from,
        date_to=date_to,
        user_name=user_name
    )
    
    return SnippetsResponse(snippets=snippets)