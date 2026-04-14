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
    unit: str = ""
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

# A representation of a single track, which the AI will return
class RecommendedTrack(BaseModel):
    id: str
    title: str
    category: Literal['sleep', 'focus', 'relaxation']

# The final response from the recommendation endpoint
class SoundTherapyRecommendationResponse(BaseModel):
    recommendationReason: str
    recommendedTracks: List[RecommendedTrack]

class HeaderCard(BaseModel):
    title: str
    currentValue: str
    unit: str
    statusText: str
    progressPercent: int

class GenericMetricDetailResponse(BaseModel):
    headerCard: HeaderCard
    insights: List[InsightCard]
    weeklyChart: List[ChartDataPoint]
    recommendations: List[RecommendationChecklistItem]

# --- Sub-indicator on a detail screen (e.g., "Heart Fitness" card) ---
class SubIndicatorCard(BaseModel):
    title: str
    status: str            # e.g., "Good shape"
    description: str       # e.g., "Your heart adapts well to rest"
    metric_label: str      # e.g., "Based on your heart rate"
    value_display: str     # e.g., "45 ms"
    color_theme: str       # "green", "red", "orange", "blue"

# --- Detail Screen Response ---
class HealthIndicatorDetailResponse(BaseModel):
    category_name: str
    overall_score: int
    header_status: str     # e.g., "Doing well today"
    header_description: str 
    info_box_text: str     # "What this means" content
    sub_indicators: List[SubIndicatorCard]
    charts: List[WeeklyReportCard] # Re-using the chart model from previous files
    ai_advice: str         # The "What you can do" section at the bottom

# --- Main Indicators Grid (10 categories) ---
class IndicatorGridItem(BaseModel):
    id: str
    title: str
    status_text: str       # e.g., "Recovering"
    score: int
    button_text: str       # e.g., "Breathing reset"

class HealthIndicatorsSummaryResponse(BaseModel):
    health_score: int
    grid_items: List[IndicatorGridItem]