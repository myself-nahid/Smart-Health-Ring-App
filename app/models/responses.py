from pydantic import BaseModel
from typing import List, Optional

class Recommendation(BaseModel):
    title: str
    description: str
    action_type: str # e.g., "nutrition", "activity", "sound_therapy"

class InsightResponse(BaseModel):
    status: str
    overall_score_estimate: int
    insights: List[str]
    recommendations: List[Recommendation]

class ChatResponse(BaseModel):
    reply: str

class AlertPrediction(BaseModel):
    risk_level: str # "Low", "Medium", "High"
    predicted_issue: str
    warning_message: str
    suggested_action: str