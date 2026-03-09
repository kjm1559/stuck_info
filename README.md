# Stock News API

FastAPI 기반 주식 뉴스 집계 시스템입니다.

## 빠른 시작

```bash
# 인프라 시작
docker compose up -d

# 데이터베이스 초기화
alembic upgrade head

# API 서버 시작
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Celery worker (별도 terminal)
celery -A app.celery worker -l info

# Celery Beat (별도 terminal)  
celery -A app.celery beat -l info
```

## 설정

```bash
cp .env.example .env
```

`.env`에 API 키 추가:
```
FINNHUB_API_KEY=your_key_here
```

## API 엔드포인트

- `GET /api/v1/health` - 헬스 체크
- `GET /api/v1/articles` - 뉴스 목록 (페이지네이션 + 필터)
- `GET /api/v1/articles/{id}` - 단일 뉴스 조회
- `GET /api/v1/companies` - 기업 목록

## 구조

```
stock_info/
├── app/
│   ├── api/          # FastAPI routes
│   ├── collectors/   # 뉴스 수집기
│   ├── celery.py     # Celery 설정
│   ├── config.py     # 설정
│   ├── tasks.py      # Celery 작업
│   └── models.py     # SQLAlchemy 모델
├── alembic/          # 마이그레이션
├── tests/            # 테스트
└── docker-compose.yml
```

## 데이터베이스 스키마

- `companies`: 주식 정보
- `articles`: 뉴스 콘텐츠 (SHA-256 중복 제거)
- `article_companies`: Many-to-many 관계

## Celery 작업

- `collect_news_for_all_companies`: 5 분마다 실행
- `cleanup_old_articles`: 매일 오전 3 시 실행 (90 일 이상 삭제)
