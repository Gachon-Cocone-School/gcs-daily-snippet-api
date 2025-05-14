from datetime import date
from typing import List, Optional
from app.db.supabase import supabase
from app.schemas.snippet import SnippetCreate, Snippet, SnippetExpanded
from postgrest import APIError

class SnippetService:
    @staticmethod
    async def create_snippet(snippet: SnippetCreate) -> Snippet:
        # First, get team info from teams table using api_id
        team_result = supabase.table("teams").select("team_name,emails").eq("api_id", snippet.api_id).execute()
        
        if not team_result.data:
            raise ValueError(f"Invalid api_id: {snippet.api_id}")

        team = team_result.data[0]
        team_name = team["team_name"]
        
        # Check if user_email is in the team's emails list
        if snippet.user_email not in team["emails"]:
            raise ValueError(f"User {snippet.user_email} is not a member of team")
        
        data = {
            "user_email": snippet.user_email,
            "team_name": team_name,
            "snippet_date": snippet.snippet_date.isoformat(),
            "content": snippet.content
        }
        
        try:
            result = supabase.table("snippets").insert(data).execute()
            return Snippet(**result.data[0])
        except APIError as e:
            error_data = e.json()  # APIError의 JSON 데이터를 가져옴
            if error_data.get('code') == '23505':  # PostgreSQL unique violation error code
                raise ValueError(f"Snippet already exists for user {snippet.user_email} on date {snippet.snippet_date}")
            raise ValueError(f"Database error: {error_data.get('message', str(e))}")
        except Exception as e:
            raise ValueError(f"Unexpected error: {str(e)}")

    @staticmethod
    async def get_snippets(
        team_name: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        user_email: Optional[str] = None
    ) -> List[SnippetExpanded]:
        query = supabase.table("snippets_expanded").select("*")

        if team_name:
            query = query.cs("team_alias", [team_name])
        if date_from:
            query = query.gte("snippet_date", date_from.isoformat())
        if date_to:
            query = query.lte("snippet_date", date_to.isoformat())
        if user_email:
            query = query.eq("user_email", user_email)

        try:
            result = query.execute()
            return [SnippetExpanded(**item) for item in result.data]
        except Exception as e:
            raise ValueError(f"Error fetching snippets: {str(e)}")

