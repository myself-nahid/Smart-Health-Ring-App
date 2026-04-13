from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Literal

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

class DashboardDataRequest(BaseModel):
    user_profile: UserProfile
    daily_health_data: DailyHealthData
    # The backend MUST provide historical data for trends
    weekly_avg_data: Optional[DailyHealthData] = None

class MetricHistoryRequest(BaseModel):
    user_profile: UserProfile
    metric: Literal['heart_rate', 'distance', 'active_time', 'calories_burned']
    # The app would send the date the user has selected.
    selected_date_str: str = "2026-04-13"

class GenericMetricRequest(BaseModel):
    user_profile: UserProfile
    # We define all possible metrics the user can tap on
    metric: Literal[
        'heart_rate', 'hrv', 'spo2', 'active_time', 'sleep_duration',
        'sleep_quality', 'stress_level', 'menstrual_cycle',
        'calories_burned', 'recovery', 'sleep_stages'
    ]