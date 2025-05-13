#!/usr/bin/env python3

import argparse
import os
from dotenv import load_dotenv
from supabase import create_client
from typing import List

# .env 파일 로드
load_dotenv()

def read_email_list(file_path: str) -> List[str]:
    """텍스트 파일에서 이메일 주소 목록을 읽어옵니다."""
    try:
        with open(file_path, 'r') as file:
            # 파일을 읽고, 각 줄의 앞뒤 공백을 제거하고, 빈 줄은 필터링합니다
            emails = [line.strip() for line in file if line.strip()]
        return emails
    except FileNotFoundError:
        print(f"오류: 파일 '{file_path}'을 찾을 수 없습니다.")
        return []
    except Exception as e:
        print(f"파일 읽기 오류: {e}")
        return []

def save_to_supabase(description: str, emails: List[str]) -> bool:
    """이메일 목록을 Supabase에 저장합니다."""
    try:
        # Supabase 클라이언트 초기화
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL과 SUPABASE_KEY 환경 변수가 필요합니다.")
        
        supabase = create_client(supabase_url, supabase_key)
        
        # 각 이메일을 데이터베이스에 삽입
        data = [{"email": email, "description": description} for email in emails]
        result = supabase.table('allowed_emails').insert(data).execute()
        
        print(f"'{description}' 목록에 {len(emails)}개의 이메일이 성공적으로 저장되었습니다.")
        return True
        
    except Exception as e:
        print(f"Supabase 저장 오류: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='이메일 목록을 Supabase에 업로드합니다.')
    parser.add_argument('file_path', help='이메일 주소가 들어있는 텍스트 파일 경로')
    parser.add_argument('description', help='이메일 목록에 대한 설명')
    
    args = parser.parse_args()
    
    # 이메일 주소 읽기
    emails = read_email_list(args.file_path)
    
    if not emails:
        print("업로드할 이메일이 없습니다.")
        return
    
    print(f"총 {len(emails)}개의 이메일 주소를 읽었습니다.")
    
    # Supabase에 저장
    save_to_supabase(args.description, emails)

if __name__ == "__main__":
    main()
