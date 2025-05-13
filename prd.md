# script 기능들

- firestore 에 아래와 같은 collection 이 있어.

  - allow_lists 컬렉션 이름
  - field
    - list_name : string
    - emails : string array

- txt 파일에 cr 로 분리된 email 주소리스트가 있어.

- txt 파일을 읽어서 firestore 에 저장해주는 콘솔용 파이썬 코드를 작성하시오.

- team-info.yaml 에 저장된 팀정보를 firestores 에 teams 컲렉션에 저장하는 콘솔용 파이썬 코드를 작성하시오.

# api 서버 기능

## 기술스펙

- python
- FastAPI
- Firestore
- Swagger docs
- fastAPI 로 개발되는 API 서버의 표준 폴더 구조를 따를 것
- 인증은 없음

## firestore 구조

- snippets 컬렉션

  - index 된 필드값
    - date : "2025-05-03" 같은 형태의 string
    - teamName: string
    - userId: string

- users 컬렉션

  - userId : string ( 복잡한 해시값으로 실제로는 안 쓰임 )
  - displayName : string ( 여기에 user_name 이 포함되어 있음 )

- teams 컬렉션
  - teamName : string
  - teamAlias : string array
  - emails : string array

## api 기능

- 주어진 파라미터에 해당하는 snippet 을 조회하여 줌
- 파라미터

  - team_name : string, mandatory
  - date_from : string, optional ( 생략되면 2000-01-01 )
  - date_to : string, optional ( 생략되면 today )
  - user_name : string, optional ( 생략될 경우는 모든 user 에 대해서 )

- return 값은 아래의 속성값을 갖는 array 임.

  - teamName
  - date
  - userName
  - snippet

- team_name 처리 방법

  - 파라미터에 있는 team_name 은 teams 컬렉션에 있는 teamAlias 에 포함되어 있는지 체크해야 한다.
  - 러턴값에는 파라미터에서 받은 team_name 을 리턴해야 함

- user_name 처리 방법

  - snippets 도큐먼트에 있는 userId 에 해당하는 displayName 을 users 컬렉션에서 가져와야 함. ( 여기에 user_name 이 포함되어 있음 )
  - 파라미터에 있는 user_name 을 displayName 에 포함되어 있는지 체크해서 필터링
  - 리턴값의 userName 에는 파라미터로 받은 user_name 대신 displayName 을 리턴해야함.

- 성능 향상을 위해 프로그램 시작시 teams 컬렉션과 users 컬렉션을 모두 읽어 캐싱한다.

## script 추가

아래 처럼 firebase 의 snippets 컬렉션에 데이터가 들어가 있어.

```
created_at
2025년 5월 9일 오후 5시 52분 25초 UTC+9
(타임스탬프)


date
"2025-05-09"
(문자열)


modified_at
2025년 5월 9일 오후 5시 52분 25초 UTC+9
(타임스탬프)


snippet
"# 오늘 한 일 - [ ] 피벗 방향성을 잡기 위한 회의 진행 - [ ] 마케팅 수업 - 차키케이스 시제품 제작 관련 논의 # 메모 - [ ] '닭'에 대해 깊게 스터디하기로 결정. - [ ] 차키 케이스 시제품 제작 -> 원데이 클래스 예약하여 빠르게 제작"
(문자열)


snippetId
"5G5ecQ9qD8PfXTYP53PQrQL729D3_2025-05-09"
(문자열)


teamName
"6기-4팀"
(문자열)


userEmail
"yoojm0220@gachon.ac.kr"
(문자열)


userId
"5G5ecQ9qD8PfXTYP53PQrQL729D3"
(문자열)
```

---

위의 데이터를 supabase 에 snippets 라는 테이블에 insert 하고 싶어. 이를 구현하는 파이썬 스크립트 짜줘. supabase 의 테이블 구조는 아래와 같아.

---

snippets

user_email text
team_name text
snippet_date date
content text
created_at timestamptz
updated_at timestamptz

---
