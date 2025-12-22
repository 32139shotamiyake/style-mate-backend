FROM python:3.10-slim

WORKDIR /app

# 依存関係
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリ本体
COPY . .

ENV FLASK_ENV=production

# Waitress で起動
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "wsgi:app"]
