from fastapi import APIRouter
from app.models.requests import DashboardDataRequest
from app.models.responses import DashboardResponse
from app.services.openai_client import generate_json_response
from app.prompts.dashboard_prompts import get_dashboard_generation_prompt
from app.services.analysis_engine import format_health_data_for_prompt

router = APIRouter()

@router.post("/generate-metrics", response_model=DashboardResponse)
async def dashboard_metrics_endpoint(payload: DashboardDataRequest):
    system_prompt = get_dashboard_generation_prompt(payload.user_profile.language)

    # Format the user data into a string for the prompt
    daily_data_str = format_health_data_for_prompt(payload.daily_health_data)
    weekly_data_str = "No weekly data available"
    if payload.weekly_avg_data:
        weekly_data_str = format_health_data_for_prompt(payload.weekly_avg_data)
    
    user_context_for_prompt = f"""
    Analyze the following User Data and generate the complete dashboard JSON.
    ---
    User Profile: {payload.user_profile.model_dump_json()}
    ---
    Today's Data:
    {daily_data_str}
    ---
    Last 7-Day Average Data:
    {weekly_data_str}
    ---
    """

    # AI will return the perfectly formatted JSON
    result_dict = await generate_json_response(system_prompt, user_context_for_prompt)

    # Pydantic validates the AI's response against our models, ensuring safety
    return DashboardResponse(**result_dict)