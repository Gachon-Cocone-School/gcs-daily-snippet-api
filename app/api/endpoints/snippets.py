from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import date
from app.schemas.snippet import SnippetCreate, Snippet, SnippetRequest, SnippetsResponse
from app.services.snippet_service import SnippetService

router = APIRouter()

@router.post("/snippets/", response_model=Snippet)
async def create_snippet(snippet: SnippetCreate):
    try:
        return await SnippetService.create_snippet(snippet)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/snippets/", response_model=SnippetsResponse)
async def get_snippets(
    team_name: str = None,
    date_from: date = None,
    date_to: date = None,
    user_email: str = None
):
    try:
        snippets = await SnippetService.get_snippets(
            team_name=team_name,
            date_from=date_from,
            date_to=date_to,
            user_email=user_email
        )
        return SnippetsResponse(snippets=snippets)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/team-snippets/", response_model=SnippetsResponse)
async def get_team_snippets(
    api_id: str,
    date_from: date = None,
    date_to: date = None
):
    try:
        snippets = await SnippetService.get_team_snippets(
            api_id=api_id,
            date_from=date_from,
            date_to=date_to
        )
        return SnippetsResponse(snippets=snippets)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))