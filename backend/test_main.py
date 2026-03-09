import sys
import os
# מוסיף את התיקייה הנוכחית לנתיב של פייתון
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_survey_analysis_positive():
    response = client.post("/submit-survey", json={
        "user_id": 1,
        "profession": "Engineer",
        "hobbies": ["coding"],
        "looking_for": "serious",
        "bio": "I am a very happy and positive person!"
    })
    assert response.status_code == 200
    assert "חיובי" in response.json()["message"]

def test_survey_analysis_negative():
    response = client.post("/submit-survey", json={
        "user_id": 2,
        "profession": "None",
        "hobbies": [],
        "looking_for": "casual",
        "bio": "I hate everything and I am very sad."
    })
    assert response.status_code == 200 # הוספתי את זה ליתר ביטחון
    assert "שלילי" in response.json()["message"]