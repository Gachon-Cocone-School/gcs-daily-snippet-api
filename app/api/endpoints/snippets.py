from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import date
from app.schemas.snippet import SnippetCreate, Snippet, SnippetRequest, SnippetsResponse
from app.services.snippet_service import SnippetService

router = APIRouter()

@router.post("/snippets/", response_model=Snippet)
async def create_snippet(snippet: SnippetCreate):
    return await SnippetService.create_snippet(snippet)

@router.get("/snippets/", response_model=SnippetsResponse)
async def get_snippets(
    team_name: str = None,
    date_from: date = None,
    date_to: date = None,
    user_email: str = None
):
    snippets = await SnippetService.get_snippets(
        team_name=team_name,
        date_from=date_from,
        date_to=date_to,
        user_email=user_email
    )
    return SnippetsResponse(snippets=snippets)

@router.put("/snippets/", response_model=Snippet)
async def update_snippet(snippet: SnippetCreate):
    return await SnippetService.update_snippet(snippet)

@router.delete("/snippets/{user_email}/{snippet_date}")
async def delete_snippet(user_email: str, snippet_date: date):
    result = await SnippetService.delete_snippet(user_email, snippet_date)
    if not result:
        raise HTTPException(status_code=404, detail="Snippet not found")