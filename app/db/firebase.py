import firebase_admin
from firebase_admin import credentials, firestore
import os
from typing import Dict, List

# Initialize Firebase app
cred_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'serviceAccountKey.json')
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

# Cache for teams and users data
teams_cache: Dict = {}
users_cache: Dict = {}

def initialize_cache():
    """
    Initialize cache by loading teams and users data from Firestore
    """
    global teams_cache, users_cache
    
    # Cache teams data
    teams_ref = db.collection('teams')
    teams_docs = teams_ref.stream()
    for doc in teams_docs:
        team_data = doc.to_dict()
        team_name = team_data.get('teamName')
        if team_name:
            teams_cache[team_name] = team_data
    
    # Cache users data
    users_ref = db.collection('users')
    users_docs = users_ref.stream()
    for doc in users_docs:
        user_data = doc.to_dict()
        user_id = doc.id
        users_cache[user_id] = user_data

def get_team_by_alias(team_alias: str) -> str:
    """
    Check if team_alias exists in any team's aliases
    Returns the team name if found, None otherwise
    """
    for team_name, team_data in teams_cache.items():
        aliases = team_data.get('teamAlias', [])
        if team_alias in aliases or team_alias == team_name:
            return team_name
    return None

def get_user_display_name(user_id: str) -> str:
    """
    Get user display name from user_id
    """
    user_data = users_cache.get(user_id)
    if user_data:
        return user_data.get('displayName', '')
    return ''

def is_user_name_match(user_id: str, user_name: str) -> bool:
    """
    Check if the user_name is included in the user's displayName
    """
    display_name = get_user_display_name(user_id)
    return user_name.lower() in display_name.lower() if display_name and user_name else False