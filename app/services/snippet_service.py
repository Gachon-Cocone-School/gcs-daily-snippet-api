from app.db.firebase import db, get_team_by_alias, get_user_display_name, is_user_name_match
from app.schemas.snippet import SnippetResponse
from datetime import datetime
from typing import List, Optional

def get_snippets(
    team_name: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    user_name: Optional[str] = None
) -> List[SnippetResponse]:
    """
    Get snippets based on filter criteria
    """
    # Set default values if None
    if date_from is None:
        date_from = "2000-01-01"
    
    # Set today's date as default for date_to if not provided
    if date_to is None:
        date_to = datetime.now().strftime("%Y-%m-%d")
    
    # Create query
    snippets_ref = db.collection('snippets')
    query = snippets_ref
    
    # Filter by team name if provided
    if team_name:
        # Verify team_name exists in team aliases
        team_name_match = get_team_by_alias(team_name)
        if not team_name_match:
            return []
        # Filter by team name
        query = query.where('teamName', '==', team_name_match)
    
    # Filter by date range
    query = query.where('date', '>=', date_from).where('date', '<=', date_to)
    
    # Execute query
    snippets = query.stream()
    
    # Process results
    result = []
    for doc in snippets:
        snippet_data = doc.to_dict()
        user_id = snippet_data.get('userId')
        
        # Filter by user_name if specified
        if user_name:
            if not is_user_name_match(user_id, user_name):
                continue
        
        # Get user display name
        display_name = get_user_display_name(user_id)
        
        snippet_response = SnippetResponse(
            teamName=team_name,  # Use the original team_name from request
            date=snippet_data.get('date', ''),
            userName=display_name,
            snippet=snippet_data.get('snippet', '')
        )
        result.append(snippet_response)
    
    return result