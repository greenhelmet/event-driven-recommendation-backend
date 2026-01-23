# 1. Python 실행 환경
FROM python:3.11-slim

# 2. 작업 디렉토리
WORKDIR /app

# 3. 시스템 패키지 (DB 연동 대비)
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# 4. 의존성 목록 복사
COPY requirements.txt .

# 5. Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 6. 애플리케이션 코드 복사
COPY app ./app

# 7. 서버 실행 명령
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
