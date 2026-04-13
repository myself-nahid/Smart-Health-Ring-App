from app.models.requests import DailyHealthData

def format_health_data_for_prompt(data: DailyHealthData) -> str:
    """Transforms raw JSON into readable text for the AI context."""
    return f"""
    Heart Rate: Avg {data.heart_rate_avg} bpm | Resting {data.heart_rate_resting} bpm
    HRV (Heart Rate Variability): {data.hrv} ms
    Steps: {data.steps}
    Sleep: {data.sleep_duration_minutes} minutes | Score: {data.sleep_score}/100
    Stress Score: {data.stress_score}/100
    Additional Data: {data.additional_indicators}
    """