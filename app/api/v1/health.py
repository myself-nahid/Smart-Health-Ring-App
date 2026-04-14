from fastapi import APIRouter
from app.models.requests import DashboardDataRequest
from app.models.responses import HealthIndicatorDetailResponse, HealthIndicatorsSummaryResponse, SubIndicatorDetailResponse
from app.services.openai_client import generate_json_response
from app.prompts.indicator_prompts import get_indicator_detail_prompt, get_sub_indicator_deep_dive_prompt

router = APIRouter()

@router.post("/summary", response_model=HealthIndicatorsSummaryResponse)
async def get_health_summary(payload: DashboardDataRequest):
    # This prompt asks AI to give a high-level status for all 10 categories at once
    system_prompt = f"Generate a high-level health summary grid for 10 categories in {payload.user_profile.language}."
    user_data = payload.daily_health_data.model_dump_json()
    
    result = await generate_json_response(system_prompt, user_data)
    return HealthIndicatorsSummaryResponse(**result)

@router.post("/category-detail", response_model=HealthIndicatorDetailResponse)
async def get_category_detail(payload: DashboardDataRequest, category: str):
    # 'category' would be "Kidney Health", "Infectious", etc.
    system_prompt = get_indicator_detail_prompt(category, payload.user_profile.language)
    user_data = payload.daily_health_data.model_dump_json()
    
    result = await generate_json_response(system_prompt, user_data)
    return HealthIndicatorDetailResponse(**result)

@router.post("/sub-indicator-detail", response_model=SubIndicatorDetailResponse)
async def get_sub_indicator_detail(payload: DashboardDataRequest, sub_indicator: str):
    # 'sub_indicator' would be "Water Level", "Blood Flow", etc.
    system_prompt = get_sub_indicator_deep_dive_prompt(sub_indicator, payload.user_profile.language)
    user_data = payload.daily_health_data.model_dump_json()
    
    result = await generate_json_response(system_prompt, user_data)
    return SubIndicatorDetailResponse(**result)