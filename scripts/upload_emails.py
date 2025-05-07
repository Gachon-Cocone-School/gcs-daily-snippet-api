#!/usr/bin/env python3

import argparse
import os
import json
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# .env 파일 로드
load_dotenv()

def read_email_list(file_path):
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

def save_to_firestore(list_name, emails):
    """이메일 목록을 Firestore에 저장합니다."""
    # Firestore 초기화
    if not firebase_admin._apps:
        try:
            cred_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
            if cred_path and os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
        except Exception as e:
            print(f"Firebase 초기화 오류: {e}")
            print("참고: Firebase Admin SDK를 사용하려면 서비스 계정 키가 필요합니다.")
            print("Firebase 콘솔 -> 프로젝트 설정 -> 서비스 계정에서 새 비공개 키를 생성하고 다운로드하세요.")
            return False
    
    # Firestore 클라이언트 생성
    db = firestore.client()
    
    try:
        # 컬렉션에 문서 추가 (기존 문서가 있으면 덮어씁니다)
        db.collection('allow_lists').document().set({
            'list_name': list_name,
            'emails': emails
        })
        print(f"'{list_name}' 목록에 {len(emails)}개의 이메일이 성공적으로 저장되었습니다.")
        return True
    except Exception as e:
        print(f"Firestore 저장 오류: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='이메일 목록을 Firestore에 업로드합니다.')
    parser.add_argument('file_path', help='이메일 주소가 들어있는 텍스트 파일 경로')
    parser.add_argument('list_name', help='저장할 목록의 이름')
    
    args = parser.parse_args()
    
    # 이메일 주소 읽기
    emails = read_email_list(args.file_path)
    
    if not emails:
        print("업로드할 이메일이 없습니다.")
        return
    
    print(f"총 {len(emails)}개의 이메일 주소를 읽었습니다.")
    
    # Firestore에 저장
    save_to_firestore(args.list_name, emails)

if __name__ == "__main__":
    main()