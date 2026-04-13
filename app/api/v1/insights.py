from fastapi import APIRouter
from app.models.requests import InsightRequest
from app.models.responses import InsightResponse
from app.services.openai_client import generate_json_response
from app.services.analysis_engine import format_health_data_for_prompt
from app.prompts.health_prompts import get_insight_generation_prompt

router = APIRouter()

@router.post("/generate-daily", response_model=InsightResponse)
async def daily_insights_endpoint(payload: InsightRequest):
    system_prompt = get_insight_generation_prompt(payload.user_profile.language)
    
    user_context = f"Goals: {payload.user_profile.goals}. Conditions: {payload.user_profile.conditions}."
    health_data_str = format_health_data_for_prompt(payload.health_data)
    
    combined_user_data = f"{user_context}\nData:\n{health_data_str}"
    
    # AI returns perfectly formatted JSON mapped to our InsightResponse Pydantic model
    result_dict = await generate_json_response(system_prompt, combined_user_data)
    
    return InsightResponse(**result_dict)