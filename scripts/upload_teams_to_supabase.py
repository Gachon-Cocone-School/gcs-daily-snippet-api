#!/usr/bin/env python3

import argparse
import os
import yaml
from typing import List, Dict, Any
from dotenv import load_dotenv
from supabase import create_client

# .env 파일 로드
load_dotenv()

def read_team_info(file_path: str) -> List[Dict[str, Any]]:
    """YAML 파일에서 팀 정보를 읽어옵니다."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            teams = yaml.safe_load(file)
        return teams
    except FileNotFoundError:
        print(f"오류: 파일 '{file_path}'을 찾을 수 없습니다.")
        return []
    except Exception as e:
        print(f"파일 읽기 오류: {e}")
        return []

def save_teams_to_supabase(teams: List[Dict[str, Any]]) -> bool:
    """팀 정보를 Supabase에 저장합니다."""
    try:
        # Supabase 클라이언트 초기화
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL과 SUPABASE_KEY 환경 변수가 필요합니다.")
        
        supabase = create_client(supabase_url, supabase_key)
        
        # 팀 정보를 Supabase 형식으로 변환
        supabase_teams = [{
            'team_name': team['teamName'],
            'team_alias': team['teamAlias'],
            'emails': team['emails']
        } for team in teams]
        
        # 모든 팀 정보를 한 번에 삽입
        result = supabase.table('teams').insert(supabase_teams).execute()
        
        print(f"총 {len(teams)}개의 팀 정보가 Supabase에 저장되었습니다.")
        return True
        
    except Exception as e:
        print(f"Supabase 저장 오류: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='팀 정보를 YAML 파일에서 읽어 Supabase에 업로드합니다.')
    parser.add_argument('--file', default='team-info.yaml', help='팀 정보가 들어있는 YAML 파일 경로 (기본값: team-info.yaml)')
    
    args = parser.parse_args()
    
    # 팀 정보 읽기
    teams = read_team_info(args.file)
    
    if not teams:
        print("업로드할 팀 정보가 없습니다.")
        return
    
    print(f"총 {len(teams)}개의 팀 정보를 읽었습니다.")
    
    # 팀 정보 출력 (확인용)
    for i, team in enumerate(teams, 1):
        print(f"\n{i}. {team['teamName']} ({', '.join(team['teamAlias'])})")
        print(f"   멤버: {', '.join(team['emails'])}")
    
    # 사용자 확인
    confirm = input("\n위 팀 정보를 Supabase에 업로드하시겠습니까? (y/n): ")
    if confirm.lower() != 'y':
        print("업로드가 취소되었습니다.")
        return
    
    # Supabase에 저장
    save_teams_to_supabase(teams)

if __name__ == "__main__":
    main()
