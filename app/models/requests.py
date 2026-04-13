from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class UserProfile(BaseModel):
    age: int
    gender: str
    language: str = Field(default="French", description="French or English")
    conditions: List[str] = Field(default_factory=list, description="e.g.,['Diabetes', 'Mental health issues']")
    goals: List[str] = Field(default_factory=list, description="e.g., ['Better Sleep', 'Stress & Mind']")

class DailyHealthData(BaseModel):
    heart_rate_avg: Optional[int] = None
    heart_rate_resting: Optional[int] = None
    hrv: Optional[int] = None
    steps: Optional[int] = None
    sleep_duration_minutes: Optional[int] = None
    sleep_score: Optional[int] = None
    stress_score: Optional[int] = None
    # Can scale up to the 28 indicators mentioned in BISO docs
    additional_indicators: Optional[Dict[str, float]] = None

class InsightRequest(BaseModel):
    user_profile: UserProfile
    health_data: DailyHealthData

class ChatMessage(BaseModel):
    role: str = Field(..., description="user or assistant")
    content: str

class ChatRequest(BaseModel):
    user_profile: UserProfile
    message: str
    chat_history: List[ChatMessage] = Field(default_factory=list)

class PredictionRequest(BaseModel):
    user_profile: UserProfile
    weekly_health_data: List[DailyHealthData]