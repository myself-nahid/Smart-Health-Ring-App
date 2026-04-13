from pydantic import BaseModel
from typing import List, Optional, Literal

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

class Trend(BaseModel):
    direction: Literal['up', 'down', 'stable']
    value: float
    unit: str
    period: str # e.g., "this week"

class CallToAction(BaseModel):
    text: str
    actionIdentifier: str # A machine-readable ID for the app

class DashboardCard(BaseModel):
    statusLabel: str
    insightDetail: str
    trend: Trend
    callToAction: CallToAction

class DashboardMetrics(BaseModel):
    mentalHealth: DashboardCard
    heartHealth: DashboardCard
    sleep: DashboardCard
    physicalActivity: DashboardCard

class DashboardResponse(BaseModel):
    healthScore: int
    scoreTitle: str
    dashboardMetrics: DashboardMetrics