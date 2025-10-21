# syntax=docker/dockerfile:1
FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 작업 디렉터리를 image-service 폴더로 맞춥니다
WORKDIR /app/image-service

# (선택) 시스템 패키지가 필요하면 여기에 apt-get 설치 추가

# 1) 의존성만 먼저 복사해 캐시 활용
COPY image-service/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# 2) 애플리케이션 코드 복사
COPY image-service/ ./

# FastAPI 기본 포트
ENV PORT=8000

# uvicorn으로 src/main.py의 app 실행
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]