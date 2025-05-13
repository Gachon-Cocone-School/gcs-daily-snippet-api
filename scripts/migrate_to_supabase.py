import firebase_admin
from firebase_admin import credentials, firestore
from supabase import create_client
from datetime import datetime
from dateutil.parser import parse
import os
from typing import Dict, Any
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv(dotenv_path=".env")

# Firebase 초기화
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Supabase 클라이언트 초기화
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL과 SUPABASE_KEY 환경 변수가 필요합니다.")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def convert_timestamp(timestamp: Any) -> datetime:
    """Firebase Timestamp 또는 문자열을 datetime 객체로 변환"""
    if hasattr(timestamp, 'timestamp'):  # Firebase Timestamp 객체인 경우
        return datetime.fromtimestamp(timestamp.timestamp())
    # 문자열인 경우 파싱
    return parse(timestamp)

def process_firebase_data(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Firebase 문서를 Supabase 형식으로 변환"""
    created_at = convert_timestamp(doc['created_at'])
    modified_at = convert_timestamp(doc['modified_at'])
    
    return {
        "user_email": doc['userEmail'],
        "team_name": doc['teamName'],
        "snippet_date": doc['date'],
        "content": doc['snippet'],
        "created_at": created_at.isoformat(),
        "updated_at": modified_at.isoformat(),
    }

def migrate_data():
    """Firebase에서 Supabase로 데이터 마이그레이션"""
    # Firebase에서 snippets 컬렉션의 모든 문서 가져오기
    snippets = db.collection('snippets').stream()
    
    for doc in snippets:
        data = doc.to_dict()
        try:
            # Supabase 형식으로 데이터 변환
            supabase_data = process_firebase_data(data)
            
            # Supabase에 데이터 삽입
            result = supabase.table('snippets').insert(supabase_data).execute()
            
            print(f"Successfully migrated snippet for {data['userEmail']} on {data['date']}")
            
        except Exception as e:
            print(f"Error migrating snippet: {str(e)}")
            print(f"Problematic data: {data}")

if __name__ == "__main__":
    migrate_data()
