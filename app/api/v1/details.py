from fastapi import APIRouter
from app.models.requests import DashboardDataRequest, MetricHistoryRequest # Re-use this request model
from app.models.responses import (
    MetricHistoryResponse,
    SleepDetailResponse,
    HealthDetailResponse,
    PhysicalActivityDetailResponse
)
from app.services.openai_client import generate_json_response
from app.prompts.detail_prompts import (
    get_metric_history_prompt,
    get_sleep_detail_prompt,
    get_health_detail_prompt,
    get_physical_activity_detail_prompt
)

router = APIRouter()

def format_data_for_prompt(payload: DashboardDataRequest) -> str:
    # Helper to create the user data context string for the AI
    daily_data_str = payload.daily_health_data.model_dump_json()
    weekly_data_str = "No weekly data available"
    if payload.weekly_avg_data:
        weekly_data_str = payload.weekly_avg_data.model_dump_json()
    
    return f"""
    User Profile: {payload.user_profile.model_dump_json()}
    Today's Data: {daily_data_str}
    Last 7-Day Average Data: {weekly_data_str}
    """

@router.post("/sleep", response_model=SleepDetailResponse)
async def get_sleep_details(payload: DashboardDataRequest):
    system_prompt = get_sleep_detail_prompt(payload.user_profile.language)
    user_context = format_data_for_prompt(payload)
    result_dict = await generate_json_response(system_prompt, user_context)
    return SleepDetailResponse(**result_dict)

@router.post("/mental-health", response_model=HealthDetailResponse)
async def get_mental_health_details(payload: DashboardDataRequest):
    system_prompt = get_health_detail_prompt(payload.user_profile.language, "Mental Health")
    user_context = format_data_for_prompt(payload)
    result_dict = await generate_json_response(system_prompt, user_context)
    return HealthDetailResponse(**result_dict)

@router.post("/heart-health", response_model=HealthDetailResponse)
async def get_heart_health_details(payload: DashboardDataRequest):
    system_prompt = get_health_detail_prompt(payload.user_profile.language, "Heart Health")
    user_context = format_data_for_prompt(payload)
    result_dict = await generate_json_response(system_prompt, user_context)
    return HealthDetailResponse(**result_dict)

@router.post("/physical-activity", response_model=PhysicalActivityDetailResponse)
async def get_physical_activity_details(payload: DashboardDataRequest):
    system_prompt = get_physical_activity_detail_prompt(payload.user_profile.language)
    user_context = format_data_for_prompt(payload)
    result_dict = await generate_json_response(system_prompt, user_context)
    return PhysicalActivityDetailResponse(**result_dict)

@router.post("/metric-history", response_model=MetricHistoryResponse)
async def get_metric_history(payload: MetricHistoryRequest):
    # The 'format_data_for_prompt' helper is not strictly needed here, 
    # as the AI is generating synthetic historical data, but you could include it
    # if you want the synthesis to be based on the user's recent averages.
    user_context = f"""
    User Profile: {payload.user_profile.model_dump_json()}
    Selected Date: {payload.selected_date_str}
    """
    
    system_prompt = get_metric_history_prompt(payload.user_profile.language, payload.metric)
    
    result_dict = await generate_json_response(system_prompt, user_context)

    return MetricHistoryResponse(**result_dict)