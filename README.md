# Daily Snippets Backend

A FastAPI application for retrieving team snippets with various filtering options.

## 기술 스펙 (Technical Specifications)

- **Python**: Core language
- **FastAPI**: Web framework
- **Firestore**: Database
- **Swagger docs**: API documentation

## 기능 (Features)

- 주어진 파라미터에 해당하는 snippet을 조회
- 팀명, 날짜 범위, 사용자명에 따른 필터링 기능 제공
- 성능 향상을 위한 teams, users 컬렉션 캐싱

## 설치 (Installation)

### 필수 조건 (Prerequisites)

- Python 3.9+
- Firestore 계정 및 serviceAccountKey.json

### 설치 방법 (Setup)

1. 저장소 클론 (Clone the repository)

```bash
git clone https://github.com/Gachon-Cocone-School/gcs-daily-snippet-api
cd gcs-daily-api
```

2. 의존성 설치 (Install dependencies)

```bash
pip install -r requirements.txt
```

3. serviceAccountKey.json 파일 프로젝트 루트에 위치 (Place the serviceAccountKey.json file in the project root)

## 실행 (Usage)

### 로컬 개발 서버 실행 (Run development server)

```bash
python main.py
```

또는 포트 지정 (or specify a port):

```bash
PORT=5000 python main.py
```

### API 엔드포인트 (API Endpoint)

- **GET /snippets**: 스니펫 조회 API

#### 파라미터 (Parameters)

- **team_name** (string, 필수): 팀 이름 또는 별칭
- **date_from** (string, 선택): 시작 날짜 (기본값: "2000-01-01")
- **date_to** (string, 선택): 종료 날짜 (기본값: 오늘)
- **user_name** (string, 선택): 필터링할 사용자 이름

#### 응답 형식 (Response Format)

```json
{
  "snippets": [
    {
      "teamName": "string",
      "date": "string",
      "userName": "string",
      "snippet": "string"
    }
  ]
}
```

### Swagger 문서 (Swagger Documentation)

API 문서는 서버 실행 후 다음 URL에서 확인할 수 있습니다:

```
http://localhost:[PORT]/docs
```

## 프로젝트 구조 (Project Structure)

```
├── main.py                    # 애플리케이션 진입점
├── requirements.txt           # 의존성 목록
├── serviceAccountKey.json     # Firebase 인증 키
├── app/
│   ├── api/                   # API 정의
│   │   ├── api.py             # API 라우터
│   │   └── endpoints/         # 엔드포인트 모듈
│   │       └── snippets.py    # 스니펫 조회 엔드포인트
│   ├── db/                    # 데이터베이스 관련
│   │   └── firebase.py        # Firebase 연결 및 캐싱
│   ├── schemas/               # Pydantic 스키마
│   │   └── snippet.py         # 스니펫 요청/응답 스키마
│   └── services/              # 비즈니스 로직
│       └── snippet_service.py # 스니펫 조회 서비스
└── scripts/                   # 유틸리티 스크립트
    ├── upload_emails.py       # 이메일 업로드 스크립트
    └── upload_teams.py        # 팀 정보 업로드 스크립트
```

## Firestore 데이터 구조 (Firestore Data Structure)

### snippets 컬렉션 (Collection)

- **date**: 날짜 (예: "2025-05-03")
- **teamName**: 팀 이름
- **userId**: 사용자 ID
- **content**: 스니펫 내용

### users 컬렉션 (Collection)

- **userId**: 사용자 ID (문서 ID)
- **displayName**: 표시 이름 (user_name 포함)

### teams 컬렉션 (Collection)

- **teamName**: 팀 이름
- **teamAlias**: 팀 별칭 배열
- **emails**: 이메일 배열

## 문의 사항

김남주(namjookim@gachon.ac.kr) 에게 문의 요망
