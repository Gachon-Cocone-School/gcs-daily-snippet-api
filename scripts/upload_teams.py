#!/usr/bin/env python3

import argparse
import os
import yaml
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

def read_team_info(file_path):
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

def save_teams_to_firestore(teams):
    """팀 정보를 Firestore에 저장합니다."""
    # Firestore 초기화
    if not firebase_admin._apps:
        try:
            # 서비스 계정 키 파일 경로 확인
            cred_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') or 'serviceAccountKey.json'
            if os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
            else:
                print(f"오류: 서비스 계정 키 파일 '{cred_path}'을 찾을 수 없습니다.")
                return False
        except Exception as e:
            print(f"Firebase 초기화 오류: {e}")
            print("참고: Firebase Admin SDK를 사용하려면 서비스 계정 키가 필요합니다.")
            print("Firebase 콘솔 -> 프로젝트 설정 -> 서비스 계정에서 새 비공개 키를 생성하고 다운로드하세요.")
            return False
    
    # Firestore 클라이언트 생성
    db = firestore.client()
    
    try:
        # 각 팀을 Firestore에 추가
        for team in teams:
            # 팀 문서 추가
            team_ref = db.collection('teams').document()
            team_ref.set({
                'teamName': team['teamName'],
                'teamAlias': team['teamAlias'],
                'emails': team['emails']
            })
            print(f"'{team['teamName']}' 팀 정보가 성공적으로 저장되었습니다.")
        
        print(f"총 {len(teams)}개의 팀 정보가 Firestore에 저장되었습니다.")
        return True
    except Exception as e:
        print(f"Firestore 저장 오류: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='팀 정보를 YAML 파일에서 읽어 Firestore에 업로드합니다.')
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
    confirm = input("\n위 팀 정보를 Firestore에 업로드하시겠습니까? (y/n): ")
    if confirm.lower() != 'y':
        print("업로드가 취소되었습니다.")
        return
    
    # Firestore에 저장
    save_teams_to_firestore(teams)

if __name__ == "__main__":
    main()