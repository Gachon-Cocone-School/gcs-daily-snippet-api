from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date as date_type, datetime

class SnippetBase(BaseModel):
    user_email: str
    team_name: str
    snippet_date: date_type
    content: str

class SnippetCreate(SnippetBase):
    pass

class Snippet(SnippetBase):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SnippetRequest(BaseModel):
    team_name: Optional[str] = None
    date_from: Optional[date_type] = Field(default=date_type(2000, 1, 1))
    date_to: Optional[date_type] = None
    user_email: Optional[str] = None

class SnippetsResponse(BaseModel):
    snippets: List[Snippet] = []