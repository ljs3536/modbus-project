FROM python:3.10-slim

WORKDIR /app

# 라이브러리 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스코드 복사 및 실행
COPY emulator.py .
CMD ["python", "-u", "emulator.py"]