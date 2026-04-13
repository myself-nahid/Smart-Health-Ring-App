from fastapi import APIRouter, HTTPException
from app.models.requests import PredictionRequest
from app.models.responses import AlertPrediction
from app.services.openai_client import generate_json_response
from openai import APIError, APITimeoutError

router = APIRouter()

@router.post("/analyze-risk", response_model=AlertPrediction)
async def risk_prediction_endpoint(payload: PredictionRequest):
    try:
        system_prompt = f"""
        You are the BISO early warning system. Review the user's past 7 days of health data.
        Look for patterns of fatigue, elevated resting heart rate, plummeting HRV, or high stress.
        Return JSON with keys: "risk_level" (Low/Medium/High), "predicted_issue" (e.g. "Fatigue / Potential Illness"), "warning_message" in {payload.user_profile.language}, and "suggested_action" in {payload.user_profile.language}.
        """
        
        weekly_data_dump =[data.model_dump() for data in payload.weekly_health_data]
        user_data = f"Profile: {payload.user_profile.model_dump()}\nWeekly Data: {weekly_data_dump}"
        
        result_dict = await generate_json_response(system_prompt, user_data)
        
        return AlertPrediction(**result_dict)
    except APITimeoutError as e:
        raise HTTPException(status_code=504, detail=f"AI service timeout: {str(e)}")
    except APIError as e:
        raise HTTPException(status_code=503, detail=f"AI service temporarily unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")