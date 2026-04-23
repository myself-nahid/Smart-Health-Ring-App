from fastapi import APIRouter
from app.models.requests import DashboardDataRequest
from app.models.responses import DashboardResponse
from app.services.openai_client import generate_json_response
from app.prompts.dashboard_prompts import get_dashboard_generation_prompt
from app.services.analysis_engine import format_health_data_for_prompt
import json

router = APIRouter()

def extract_metric_comparison(daily_data, weekly_data) -> str:
    """Extract detailed metric comparisons between daily and weekly averages."""
    comparisons = {}
    daily_dict = daily_data.model_dump()
    weekly_dict = weekly_data.model_dump() if weekly_data else {}
    
    metric_fields = [
        'heart_rate_avg', 'heart_rate_resting', 'hrv', 'steps', 
        'sleep_duration_minutes', 'sleep_score', 'stress_score'
    ]
    
    for field in metric_fields:
        daily_val = daily_dict.get(field)
        weekly_val = weekly_dict.get(field)
        
        if daily_val is not None and weekly_val is not None:
            try:
                change = daily_val - weekly_val
                pct_change = (change / weekly_val * 100) if weekly_val != 0 else 0
                
                # Determine direction (positive change interpretation varies by metric)
                if field in ['stress_score', 'heart_rate_resting']:
                    # For these, lower is better, so negative change is good
                    direction = 'up' if change > 0 else ('down' if change < 0 else 'stable')
                else:
                    # For positive metrics, positive change is good
                    direction = 'down' if change > 0 else ('up' if change < 0 else 'stable')
                
                comparisons[field] = {
                    'daily': daily_val,
                    'weekly_avg': weekly_val,
                    'change': round(change, 2),
                    'percent_change': round(pct_change, 1),
                    'direction': direction
                }
            except (TypeError, ZeroDivisionError):
                pass
    
    return json.dumps(comparisons, indent=2)

def create_metric_summary(daily_data, weekly_data) -> str:
    """Create a structured summary of all available metrics with context."""
    daily_dict = daily_data.model_dump()
    weekly_dict = weekly_data.model_dump() if weekly_data else {}
    
    # Define normal ranges for health metrics
    HEALTH_RANGES = {
        'heart_rate_avg': {'normal': (60, 100), 'unit': 'bpm'},
        'heart_rate_resting': {'normal': (60, 80), 'unit': 'bpm'},
        'hrv': {'normal': (20, 150), 'unit': 'ms'},
        'steps': {'normal': (5000, 10000), 'unit': 'steps'},
        'sleep_duration_minutes': {'normal': (420, 540), 'unit': 'min'},  # 7-9 hours
        'sleep_score': {'normal': (70, 100), 'unit': '/100'},
        'stress_score': {'normal': (0, 40), 'unit': '/100'}  # Lower is better
    }
    
    summary = {
        'metrics_data': {},
        'available_metrics': [],
        'missing_metrics': [],
        'alerts': []
    }
    
    for metric, range_info in HEALTH_RANGES.items():
        if metric in daily_dict and daily_dict[metric] is not None:
            value = daily_dict[metric]
            summary['available_metrics'].append(metric)
            summary['metrics_data'][metric] = {
                'today': value,
                'weekly_avg': weekly_dict.get(metric),
                'normal_range': range_info['normal'],
                'unit': range_info['unit'],
                'is_normal': range_info['normal'][0] <= value <= range_info['normal'][1]
            }
            
            # Flag concerning values
            if not summary['metrics_data'][metric]['is_normal']:
                if metric in ['stress_score', 'heart_rate_resting']:
                    if value > range_info['normal'][1]:
                        summary['alerts'].append(f"{metric} is elevated ({value})")
                else:
                    if value < range_info['normal'][0]:
                        summary['alerts'].append(f"{metric} is low ({value})")
        else:
            summary['missing_metrics'].append(metric)
    
    return json.dumps(summary, indent=2)

@router.post("/generate-dashboard-metrics", response_model=DashboardResponse)
async def generate_dashboard_metrics(payload: DashboardDataRequest):
    """Generate the dashboard cards payload for the mobile app."""
    system_prompt = get_dashboard_generation_prompt(payload.user_profile.language)

    # Format the user data into a string for the prompt
    daily_data_str = format_health_data_for_prompt(payload.daily_health_data)
    weekly_data_str = "No weekly data available"
    if payload.weekly_avg_data:
        weekly_data_str = format_health_data_for_prompt(payload.weekly_avg_data)
    
    # Extract comprehensive metric comparisons
    metric_comparison = extract_metric_comparison(payload.daily_health_data, payload.weekly_avg_data)
    
    # Create detailed metric summary with ranges and alerts
    metric_summary = create_metric_summary(payload.daily_health_data, payload.weekly_avg_data)
    
    user_context_for_prompt = f"""
    ANALYZING COMPLETE USER DATA FOR DASHBOARD GENERATION
    
    USER PROFILE:
    {payload.user_profile.model_dump_json(indent=2)}
    
    TODAY'S HEALTH DATA:
    {daily_data_str}
    
    7-DAY AVERAGE DATA:
    {weekly_data_str}
    
    METRIC COMPARISON (Today vs Weekly Average):
    {metric_comparison}
    
    COMPREHENSIVE METRIC SUMMARY WITH CONTEXT:
    {metric_summary}
    
    INSTRUCTIONS FOR DASHBOARD GENERATION:
    1. Analyze all available metrics above to determine overall health status.
    2. Calculate healthScore (0-100) based on how many metrics are in healthy range.
    3. Prioritize metrics that show concerning trends or significant change.
    4. For each dashboard card (Mental Health, Heart Health, Sleep, Physical Activity):
       - Use the exact metric name in "metricLabel".
       - Use "statusLabel" for the current evaluation only.
       - Provide a meaningful insight and a clear call to action.
    5. Ensure the payload matches the DashboardResponse model exactly.
    6. Use developer-friendly actionIdentifier values (camelCase).
    """

    # AI will return the perfectly formatted JSON
    result_dict = await generate_json_response(system_prompt, user_context_for_prompt)

    # Pydantic validates the AI's response against our models, ensuring safety
    return DashboardResponse(**result_dict)