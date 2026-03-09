FROM python:3.11-slim

# התקנת ספריות מערכת שדרושות עבור psycopg2 (החיבור ל-Postgres)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# הורדת המילון של TextBlob (חשוב!)
RUN python -m textblob.download_corpora

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]