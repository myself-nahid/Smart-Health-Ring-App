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

# --- Shared Components ---
class ChartDataPoint(BaseModel):
    label: str  # e.g., "M", "Jan", "Awake"
    value: float
    unit: str
    isHighlighted: Optional[bool] = False

class InsightCard(BaseModel):
    iconIdentifier: str # e.g., "brain_icon", "heart_icon", "info_icon"
    title: str
    description: str

class RecommendationChecklistItem(BaseModel):
    text: str
    isChecked: bool

# --- Sleep Detail Screen Response ---
class SleepStage(BaseModel):
    stage: Literal['Awake', 'Light', 'Deep', 'REM']
    durationMinutes: int
    percentage: int

class SleepDetailResponse(BaseModel):
    totalDuration: str
    bedTime: str
    wakeUpTime: str
    sleepScore: int
    scoreTrendText: str
    sleepStages: List[SleepStage]
    insights: List[InsightCard]
    trendChart: List[ChartDataPoint]

# --- Mental/Heart Health Detail Screen Response ---
class HealthHeaderCard(BaseModel):
    status: str
    score: int
    insightSummary: str
    progressPercent: int

class HealthDetailResponse(BaseModel):
    headerCard: HealthHeaderCard
    insights: List[InsightCard]
    weeklyChart: List[ChartDataPoint]
    recommendations: List[RecommendationChecklistItem]

# --- Physical Activity Detail Screen Response ---
class GoalProgressCard(BaseModel):
    title: str
    currentValue: float
    goalValue: float
    progressPercent: int

class StatGridItem(BaseModel):
    iconIdentifier: str
    title: str
    value: str
    unit: str

class ActivityDurationItem(BaseModel):
    day: str
    duration: str
    percentage: int

class PhysicalActivityDetailResponse(BaseModel):
    goalCard: GoalProgressCard
    statGrid: List[StatGridItem]
    progressInsight: InsightCard
    durationOfActivity: List[ActivityDurationItem]
    weeklyAverage: str

class TodaysReportCard(BaseModel):
    title: str
    value: str
    unit: str
    subtitle: str

class WeeklyReportCard(BaseModel):
    chartData: List[ChartDataPoint]
    averageValue: str

class MonthlyOverviewCard(BaseModel):
    chartData: List[ChartDataPoint]

class MetricHistoryResponse(BaseModel):
    metricName: str
    todaysReport: TodaysReportCard
    weeklyReport: WeeklyReportCard
    monthlyOverview: MonthlyOverviewCard