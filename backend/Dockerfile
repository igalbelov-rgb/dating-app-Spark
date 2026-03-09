FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# במקום main.py, אנחנו אומרים לו: חפש בקובץ main את המשתנה שנקרא app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]