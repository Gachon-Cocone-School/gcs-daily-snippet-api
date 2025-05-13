from datetime import date, datetime
from typing import List, Optional
from app.db.supabase import supabase
from app.schemas.snippet import SnippetCreate, Snippet, SnippetBase

class SnippetService:
    @staticmethod
    async def create_snippet(snippet: SnippetCreate) -> Snippet:
        data = {
            "user_email": snippet.user_email,
            "team_name": snippet.team_name,
            "snippet_date": snippet.snippet_date.isoformat(),
            "content": snippet.content
        }
        
        result = supabase.table("snippets").insert(data).execute()
        return Snippet(**result.data[0])

    @staticmethod
    async def get_snippets(
        team_name: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        user_email: Optional[str] = None
    ) -> List[Snippet]:
        query = supabase.table("snippets").select("*")

        if team_name:
            query = query.eq("team_name", team_name)
        if date_from:
            query = query.gte("snippet_date", date_from.isoformat())
        if date_to:
            query = query.lte("snippet_date", date_to.isoformat())
        if user_email:
            query = query.eq("user_email", user_email)

        result = query.execute()
        return [Snippet(**item) for item in result.data]

    @staticmethod
    async def update_snippet(snippet: SnippetCreate) -> Snippet:
        data = {
            "user_email": snippet.user_email,
            "team_name": snippet.team_name,
            "snippet_date": snippet.snippet_date.isoformat(),
            "content": snippet.content
        }
        
        result = supabase.table("snippets")\
            .update(data)\
            .eq("user_email", snippet.user_email)\
            .eq("snippet_date", snippet.snippet_date.isoformat())\
            .execute()
            
        return Snippet(**result.data[0])

    @staticmethod
    async def delete_snippet(user_email: str, snippet_date: date) -> bool:
        result = supabase.table("snippets")\
            .delete()\
            .eq("user_email", user_email)\
            .eq("snippet_date", snippet_date.isoformat())\
            .execute()
            
        return len(result.data) > 0