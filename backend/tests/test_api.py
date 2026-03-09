import pytest
from fastapi.testclient import TestClient
from main import app  # תוודא שזה הקובץ הנכון שלך

client = TestClient(app)

def test_read_root():
    """בדיקה בסיסית שהאפליקציה עובדת"""
    response = client.get("/")
    assert response.status_code == 200