# 동물이 쓴 편지 생성 서비스

K-PaaS 2025를 위한 강아지 편지 생성 이미지 서비스입니다. 강아지 사진을 업로드하면 해당 강아지의 관점에서 작성된 따뜻한 편지를 생성해줍니다.

## 서비스 개요

이 서비스는 OpenAI의 GPT-4o-mini 비전 모델을 사용하여 강아지 이미지를 분석하고, 강아지의 외모와 표정을 바탕으로 개성있는 편지를 생성합니다. 생성된 이미지는 NCloud Object Storage에 안전하게 저장됩니다.

### 주요 기능
- 🐕 강아지 이미지 업로드 및 저장
- 🤖 AI 기반 이미지 분석 및 편지 생성
- 💌 강아지 관점의 따뜻한 한국어 편지 작성
- ☁️ NCloud Object Storage 통합
- 📝 구조화된 API 응답

## 🛠️ 설치 및 설정

### 필수 요구사항
- Python 3.12+
- NCloud Object Storage 계정
- OpenAI API 키

### 1. 의존성 설치
```bash
pip install fastapi uvicorn openai boto3 python-dotenv
```

### 2. 환경 변수 설정
`src/.env.local` 파일을 생성하고 다음 내용을 입력하세요:

```bash
# NCloud Object Storage 설정
NCLOUD_ACCESS_KEY=your_access_key_here
NCLOUD_SECRET_KEY=your_secret_key_here
NCLOUD_BUCKET_NAME=your_bucket_name_here

# OpenAI 설정
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. 서비스 실행

**방법 1: uvicorn 직접 실행**
```bash
uvicorn src.main:app --reload --port 1110
```

**방법 2: 시작 스크립트 사용**
```bash
python start_server.py
```

서비스가 성공적으로 실행되면 다음 주소에서 접속할 수 있습니다:
- **API 문서**: http://localhost:1110
- **헬스 체크**: http://localhost:1110/image-service/health

## API 사용법

### 기본 URL
```
http://localhost:1110/image-service
```

### 1. 헬스 체크
```http
GET /health
```

**응답 예시:**
```json
{
  "status": 200,
  "status_text": "OK",
  "data": {"status": "healthy"},
  "message": "Service is healthy"
}
```

### 2. 강아지 편지 생성
```http
POST /generate-letter
Content-Type: multipart/form-data
```

**입력 파라미터:**
- `file`: 강아지 이미지 파일 (JPG, PNG 등)

**요청 예시 (curl):**
```bash
curl -X POST "http://localhost:1110/image-service/generate-letter" \
  -F "file=@my_dog.jpg"
```

**응답 예시:**
```json
{
  "status": 200,
  "status_text": "OK",
  "data": {
    "image_url": "https://kr.object.ncloudstorage.com/contest21/images/a1b2c3d4...f6.jpg",
    "object_key": "images/a1b2c3d4e5f6789012345678901234ab.jpg",
    "filename": "my_dog.jpg",
    "letter": "사랑하는 엄마에게,\n\n안녕하세요! 저는 여기 햇살 좋은 곳에 앉아있어요..."
  },
  "message": "Letter generated successfully"
}
```

## 입력 및 출력

### 입력
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| file | File | ✅ | 강아지 이미지 파일 (JPG, PNG, GIF 등) |

### 출력
| 필드 | 타입 | 설명 |
|------|------|------|
| status | Integer | HTTP 상태 코드 (200: 성공) |
| status_text | String | 상태 메시지 |
| data.image_url | String | 업로드된 이미지의 공개 URL |
| data.object_key | String | 스토리지 내 객체 경로 |
| data.filename | String | 원본 파일명 |
| data.letter | String | 생성된 한국어 편지 내용 |
| message | String | 처리 결과 메시지 |

## 아키텍처

```
src/
├── main.py              # FastAPI 애플리케이션 엔트리포인트
├── .env.local          # 환경 변수
├── service/
│   ├── router.py       # API 라우터 및 엔드포인트
│   └── service.py      # 비즈니스 로직
├── model/
│   ├── __init__.py     # OpenAI 클라이언트 초기화
│   └── openai_client.py # OpenAI 클라이언트 클래스
└── data/
    ├── __init__.py     # 스토리지 초기화
    └── storage.py      # NCloud Object Storage 클라이언트
```

## 처리 흐름

1. **이미지 업로드**: 사용자가 강아지 이미지를 업로드
2. **파일 검증**: 이미지 파일 타입 검증
3. **랜덤 파일명 생성**: UUID를 사용한 고유 파일명 생성
4. **스토리지 저장**: NCloud Object Storage에 이미지 저장
5. **AI 분석**: OpenAI GPT-4o-mini로 이미지 분석
6. **편지 생성**: 강아지 관점의 한국어 편지 생성
7. **결과 반환**: 이미지 URL과 편지 내용 반환

## 로깅

서비스는 구조화된 로깅을 제공합니다:

```
형식: %(asctime)s [%(levelname)s] %(name)s: %(message)s
레벨: INFO
```

**로그 예시:**
```
2025-10-05 22:26:43,336 [INFO] src.service.service: Processing image: dog.jpg -> a1b2c3d4e5f6789012345678901234ab.jpg
2025-10-05 22:26:43,835 [INFO] src.data.storage: Successfully uploaded file object to images/a1b2c3d4e5f6789012345678901234ab.jpg
2025-10-05 22:26:47,225 [INFO] src.model.openai_client: Generated letter from image URL successfully
```

## 오류 처리

### 일반적인 오류
- **400**: 잘못된 파일 형식 (이미지가 아닌 파일)
- **500**: 이미지 업로드 실패 또는 AI 처리 실패

### 환경 설정 오류
- NCloud 인증 정보 누락: `Missing required NCloud storage credentials`
- OpenAI API 키 누락: `Missing OPENAI_API_KEY environment variable`

## 개발 정보

- **Framework**: FastAPI
- **AI Model**: OpenAI GPT-4o-mini (비전)
- **Storage**: NCloud Object Storage (S3 호환)
- **Language**: Python 3.12+
