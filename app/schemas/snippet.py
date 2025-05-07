from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date as date_type

class SnippetRequest(BaseModel):
    team_name: str
    date_from: Optional[str] = Field(default="2000-01-01")
    date_to: Optional[str] = None  # Will be set to today if None
    user_name: Optional[str] = None

class SnippetResponse(BaseModel):
    teamName: str
    date: str
    userName: str
    snippet: str

class SnippetsResponse(BaseModel):
    snippets: List[SnippetResponse] = []