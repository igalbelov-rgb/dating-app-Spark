from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from textblob import TextBlob
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# זה התיקון: החלפנו את bootstrap ב-expose
Instrumentator().instrument(app).expose(app)

class UserSurvey(BaseModel):
    user_id: int
    profession: str
    hobbies: List[str]
    looking_for: str
    bio: str

@app.get("/")
def root():
    return {"status": "Spark AI Backend is running"}

@app.post("/submit-survey")
async def submit_survey(survey: UserSurvey):
    analysis = TextBlob(survey.bio)
    sentiment = "חיובי" if analysis.sentiment.polarity >= 0 else "שלילי"
    
    recommendation = "נראה שאת/ה אדם אופטימי! נחפש לך התאמות דומות." if sentiment == "חיובי" else "ה-Bio שלך נשמע קצת רציני מדי, נסה להוסיף חיוך."

    print(f"AI Analysis for user {survey.user_id}: {sentiment}")
    
    return {
        "status": "success",
        "message": f"השאלון התקבל! ניתוח AI: ה-Bio שלך {sentiment}.",
        "recommendation": recommendation
    }