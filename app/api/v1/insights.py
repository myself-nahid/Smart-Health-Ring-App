from fastapi import APIRouter, HTTPException
from app.models.requests import InsightRequest
from app.models.responses import InsightResponse
from app.services.openai_client import generate_json_response
from app.services.analysis_engine import format_health_data_for_prompt
from app.prompts.health_prompts import get_insight_generation_prompt
from openai import APIError, APITimeoutError

router = APIRouter()

@router.post("/generate-daily", response_model=InsightResponse)
async def daily_insights_endpoint(payload: InsightRequest):
    try:
        system_prompt = get_insight_generation_prompt(payload.user_profile.language)
        
        user_context = f"Goals: {payload.user_profile.goals}. Conditions: {payload.user_profile.conditions}."
        health_data_str = format_health_data_for_prompt(payload.health_data)
        
        combined_user_data = f"{user_context}\nData:\n{health_data_str}"
        
        # AI returns perfectly formatted JSON mapped to our InsightResponse Pydantic model
        result_dict = await generate_json_response(system_prompt, combined_user_data)
        
        return InsightResponse(**result_dict)
    except APITimeoutError as e:
        raise HTTPException(status_code=504, detail=f"AI service timeout: {str(e)}")
    except APIError as e:
        raise HTTPException(status_code=503, detail=f"AI service temporarily unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")