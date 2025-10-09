# Call Service API

노인 반려동물 입양 상담을 위한 음성 기반 API 서비스입니다.

## Quick Start

```bash
# 1. 의존성 설치
pip install fastapi uvicorn openai sqlalchemy mysql-connector-python python-dotenv

# 2. 환경 변수 설정 (.env 파일 생성)
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=call_service_db
OPENAI_API_KEY=your_openai_api_key

# 3. MySQL 데이터베이스 생성
CREATE DATABASE call_service_db;

# 4. 서비스 실행 (포트 1110)
uvicorn src.main:app --reload --port 1110

# 5. API 문서 확인
# http://localhost:1110
```

## 서비스 개요

음성 입력을 통해 AI 상담사가 반려동물 입양 전 필수 정보를 수집하고, 입양 후 정기 상담을 제공하는 서비스입니다.

- **기술스택**: FastAPI, OpenAI (Whisper, GPT-4o-mini, TTS), MySQL
- **포트**: 1110
- **베이스 URL**: `http://localhost:1110/call-service`

## API 명세

### 1. 헬스 체크

```http
GET /health
```

**응답**
```json
{
  "status": 200,
  "status_text": "OK",
  "data": {"status": "healthy"},
  "message": "Service is healthy"
}
```

### 2. 초기 입양 상담

```http
POST /initial-counseling
Content-Type: multipart/form-data
```

**요청 파라미터**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `audio_file` | File | ✅ | 음성 파일 (webm, mp3, wav) |
| `user_id` | String | ✅ | 사용자 고유 ID |
| `session_id` | String | ❌ | 세션 ID (없으면 자동 생성) |
| `collected_info` | String | ❌ | 기존 수집 정보 JSON (기본값: "{}") |
| `return_audio` | Boolean | ❌ | 음성 응답 반환 여부 (기본값: true) |

**응답**
```json
{
  "status": 200,
  "status_text": "SUCCESS",
  "data": {
    "user_id": "user123",
    "session_id": "uuid-string",
    "user_text": "사용자 음성을 텍스트로 변환한 내용",
    "assistant_text": "AI 상담사 응답 텍스트",
    "assistant_audio_base64": "base64로 인코딩된 음성 데이터",
    "collected_info": {
      "home_size": "25평 아파트",
      "pet_experience": "강아지 키워본 경험 있음"
    },
    "is_info_complete": false,
    "conversation_history": [...]
  },
  "message": "Initial counseling processed successfully"
}
```

### 3. 입양 후 정기 상담

```http
POST /post-adoption-checkup
Content-Type: multipart/form-data
```

**요청 파라미터**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `audio_file` | File | ✅ | 음성 파일 |
| `user_id` | String | ✅ | 사용자 고유 ID |
| `session_id` | String | ❌ | 세션 ID |
| `pet_info` | String | ❌ | 반려동물 정보 JSON (기본값: "{}") |
| `return_audio` | Boolean | ❌ | 음성 응답 반환 여부 (기본값: true) |

**응답**
```json
{
  "status": 200,
  "status_text": "SUCCESS",
  "data": {
    "user_id": "user123",
    "session_id": "uuid-string",
    "user_text": "사용자 음성 내용",
    "assistant_text": "상담사 응답",
    "assistant_audio_base64": "음성 데이터",
    "health_check": {
      "elderly_physical": "건강 상태 양호",
      "pet_health": "반려견 건강함",
      "needs_attention": false
    },
    "sentiment": "긍정적",
    "conversation_history": [...]
  },
  "message": "Regular checkup processed successfully"
}
```

### 4. 세션 종료

```http
POST /end-session
Content-Type: multipart/form-data
```

**요청 파라미터**
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `user_id` | String | ✅ | 사용자 고유 ID |
| `session_id` | String | ✅ | 종료할 세션 ID |

**응답**
```json
{
  "status": 200,
  "status_text": "SUCCESS",
  "data": {
    "session_id": "uuid-string",
    "saved": true
  },
  "message": "Session successfully ended and saved"
}
```

## 수집 정보

### 초기 상담 수집 항목
- `home_size`: 집 크기 (평수, 주택 형태)
- `mobility_health`: 거동 및 건강 상태
- `pet_experience`: 반려동물 경험
- `time_away`: 하루 평균 외출 시간
- `living_with`: 동거인 정보
- `allergies`: 알레르기 유무

### 정기 상담 분석 항목
- `elderly_physical`: 어르신 신체 건강
- `elderly_mental`: 어르신 정신 건강
- `pet_health`: 반려견 건강 상태
- `pet_behavior`: 반려견 행동 특이사항
- `daily_activities`: 일상 활동
- `positive_effects`: 긍정적 변화
- `needs_attention`: 주의 필요 여부

## 오류 코드

| 코드 | 설명 |
|------|------|
| 400 | 잘못된 요청 (빈 세션, 파라미터 오류) |
| 404 | 세션을 찾을 수 없음 |
| 500 | 서버 오류 (OpenAI API, DB 연결 실패) |

## 개발자 가이드

### 테스트 예시 (Java)

```java
import java.io.*;
import java.net.URI;
import java.net.http.*;
import java.nio.file.*;

public class CallServiceClient {
    private static final String BASE_URL = "http://localhost:1110/call-service";
    private static final HttpClient client = HttpClient.newHttpClient();

    // 1. 헬스 체크
    public static void healthCheck() throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(BASE_URL + "/health"))
            .GET()
            .build();

        HttpResponse<String> response = client.send(request,
            HttpResponse.BodyHandlers.ofString());
        System.out.println("Health Check: " + response.body());
    }

    // 2. 초기 상담 테스트
    public static void initialCounseling(String audioFilePath) throws Exception {
        String boundary = "----boundary" + System.currentTimeMillis();
        String CRLF = "\r\n";

        ByteArrayOutputStream baos = new ByteArrayOutputStream();

        // audio_file
        baos.write(("--" + boundary + CRLF).getBytes());
        baos.write(("Content-Disposition: form-data; name=\"audio_file\"; filename=\"test_audio.webm\"" + CRLF).getBytes());
        baos.write(("Content-Type: audio/webm" + CRLF + CRLF).getBytes());
        baos.write(Files.readAllBytes(Paths.get(audioFilePath)));
        baos.write(CRLF.getBytes());

        // user_id
        baos.write(("--" + boundary + CRLF).getBytes());
        baos.write(("Content-Disposition: form-data; name=\"user_id\"" + CRLF + CRLF).getBytes());
        baos.write("test_user_123".getBytes());
        baos.write(CRLF.getBytes());

        // return_audio
        baos.write(("--" + boundary + CRLF).getBytes());
        baos.write(("Content-Disposition: form-data; name=\"return_audio\"" + CRLF + CRLF).getBytes());
        baos.write("true".getBytes());
        baos.write((CRLF + "--" + boundary + "--" + CRLF).getBytes());

        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(BASE_URL + "/initial-counseling"))
            .header("Content-Type", "multipart/form-data; boundary=" + boundary)
            .POST(HttpRequest.BodyPublishers.ofByteArray(baos.toByteArray()))
            .build();

        HttpResponse<String> response = client.send(request,
            HttpResponse.BodyHandlers.ofString());
        System.out.println("Initial Counseling: " + response.body());
    }

    // 3. 정기 상담 테스트
    public static void postAdoptionCheckup(String audioFilePath) throws Exception {
        String boundary = "----boundary" + System.currentTimeMillis();
        String CRLF = "\r\n";

        ByteArrayOutputStream baos = new ByteArrayOutputStream();

        // audio_file
        baos.write(("--" + boundary + CRLF).getBytes());
        baos.write(("Content-Disposition: form-data; name=\"audio_file\"; filename=\"checkup_audio.webm\"" + CRLF).getBytes());
        baos.write(("Content-Type: audio/webm" + CRLF + CRLF).getBytes());
        baos.write(Files.readAllBytes(Paths.get(audioFilePath)));
        baos.write(CRLF.getBytes());

        // user_id
        baos.write(("--" + boundary + CRLF).getBytes());
        baos.write(("Content-Disposition: form-data; name=\"user_id\"" + CRLF + CRLF).getBytes());
        baos.write("test_user_123".getBytes());
        baos.write(CRLF.getBytes());

        // pet_info
        baos.write(("--" + boundary + CRLF).getBytes());
        baos.write(("Content-Disposition: form-data; name=\"pet_info\"" + CRLF + CRLF).getBytes());
        baos.write("{\"name\":\"멍멍이\",\"breed\":\"골든리트리버\"}".getBytes());
        baos.write((CRLF + "--" + boundary + "--" + CRLF).getBytes());

        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(BASE_URL + "/post-adoption-checkup"))
            .header("Content-Type", "multipart/form-data; boundary=" + boundary)
            .POST(HttpRequest.BodyPublishers.ofByteArray(baos.toByteArray()))
            .build();

        HttpResponse<String> response = client.send(request,
            HttpResponse.BodyHandlers.ofString());
        System.out.println("Post Adoption Checkup: " + response.body());
    }

    // 4. 세션 종료
    public static void endSession(String sessionId) throws Exception {
        String boundary = "----boundary" + System.currentTimeMillis();
        String CRLF = "\r\n";

        ByteArrayOutputStream baos = new ByteArrayOutputStream();

        // user_id
        baos.write(("--" + boundary + CRLF).getBytes());
        baos.write(("Content-Disposition: form-data; name=\"user_id\"" + CRLF + CRLF).getBytes());
        baos.write("test_user_123".getBytes());
        baos.write(CRLF.getBytes());

        // session_id
        baos.write(("--" + boundary + CRLF).getBytes());
        baos.write(("Content-Disposition: form-data; name=\"session_id\"" + CRLF + CRLF).getBytes());
        baos.write(sessionId.getBytes());
        baos.write((CRLF + "--" + boundary + "--" + CRLF).getBytes());

        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(BASE_URL + "/end-session"))
            .header("Content-Type", "multipart/form-data; boundary=" + boundary)
            .POST(HttpRequest.BodyPublishers.ofByteArray(baos.toByteArray()))
            .build();

        HttpResponse<String> response = client.send(request,
            HttpResponse.BodyHandlers.ofString());
        System.out.println("End Session: " + response.body());
    }

    // 사용 예시
    public static void main(String[] args) throws Exception {
        healthCheck();
        initialCounseling("test_audio.webm");
        postAdoptionCheckup("checkup_audio.webm");
        endSession("your_session_id");
    }
}
```

### 프로젝트 구조
```
src/
├── main.py              # FastAPI 앱 실행
├── __init__.py          # APIResponse, APIException
├── service/router.py    # API 엔드포인트
├── model/openai_client.py # OpenAI 클라이언트
└── data/database.py     # MySQL 모델
```

### 주요 로그 확인
```bash
# 서비스 실행 후 로그에서 확인할 내용:
# - "Database connection established" (DB 연결 성공)
# - "OpenAI client initialized successfully" (OpenAI 연결 성공)
# - "Processing initial counseling - user: xxx" (요청 처리)
```
