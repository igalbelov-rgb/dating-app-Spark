from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from textblob import TextBlob
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy.orm import Session
import logging

# וודא שהייבוא תואם לשמות הקבצים שלך
from .database import get_db, SurveyResult, engine, Base

logger = logging.getLogger("uvicorn")
app = FastAPI(title="Spark AI Backend")

# הגדרת המוניטורינג
Instrumentator().instrument(app).expose(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# מודלים של Pydantic לבקשות ותגובות
class UserSurvey(BaseModel):
    user_id: int
    profession: str
    hobbies: List[str]
    looking_for: str
    bio: str

class SentimentResponse(BaseModel):
    status: str
    message: str
    recommendation: str

# יצירת הטבלאות בהפעלת האפליקציה
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database tables verified/created")

@app.get("/", tags=["health"])
def root():
    return {"status": "Spark AI Backend is running", "version": "1.1"}

@app.post("/submit-survey", response_model=SentimentResponse, tags=["survey"])
def submit_survey(survey: UserSurvey, db: Session = Depends(get_db)):
    try:
        # 1. ניתוח רגשות (AI Logic)
        analysis = TextBlob(survey.bio)
        polarity = analysis.sentiment.polarity
        sentiment = "חיובי" if polarity >= 0 else "שלילי"
        
        recommendation = (
            "נראה שאת/ה אדם אופטימי! נחפש לך התאמות דומות."
            if sentiment == "חיובי"
            else "ה‑Bio שלך נשמע קצת רציני מדי, נסה להוסיף חיוך."
        )

        # 2. שמירה למסד הנתונים
        new_result = SurveyResult(
            user_id=survey.user_id,
            profession=survey.profession,
            bio=survey.bio,
            sentiment_score=polarity,
            sentiment_label=sentiment,
        )
        
        db.add(new_result)
        db.commit()
        db.refresh(new_result)

        logger.info(f"Successfully saved survey for user {survey.user_id}")

        return {
            "status": "success",
            "message": f"השאלון התקבל! ניתוח AI: ה‑Bio שלך {sentiment}.",
            "recommendation": recommendation,
        }
    except Exception as e:
        logger.error(f"Error saving survey: {str(e)}")
        raise HTTPException(status_code=500, detail="שגיאה פנימית בשמירת הנתונים")