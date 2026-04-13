from fastapi import APIRouter, HTTPException
from app.models.requests import ChatRequest
from app.models.responses import ChatResponse
from app.services.openai_client import generate_chat_response
from app.prompts.simbi_prompts import get_simbi_system_prompt
from openai import APIError, APITimeoutError

router = APIRouter()

@router.post("/simbi-chat", response_model=ChatResponse)
async def simbi_chat_endpoint(payload: ChatRequest):
    try:
        system_prompt = get_simbi_system_prompt(payload.user_profile)
        
        # Construct message array
        messages =[{"role": "system", "content": system_prompt}]
        for msg in payload.chat_history:
            messages.append({"role": msg.role, "content": msg.content})
        
        messages.append({"role": "user", "content": payload.message})
        
        # Call OpenAI
        reply = await generate_chat_response(messages)
        
        return ChatResponse(reply=reply)
    except APITimeoutError as e:
        raise HTTPException(status_code=504, detail=f"AI service timeout: {str(e)}")
    except APIError as e:
        raise HTTPException(status_code=503, detail=f"AI service temporarily unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")