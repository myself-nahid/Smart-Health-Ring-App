from fastapi import APIRouter
from app.models.requests import ChatRequest
from app.models.responses import ChatResponse
from app.services.openai_client import generate_chat_response
from app.prompts.simbi_prompts import get_simbi_system_prompt

router = APIRouter()

@router.post("/simbi-chat", response_model=ChatResponse)
async def simbi_chat_endpoint(payload: ChatRequest):
    system_prompt = get_simbi_system_prompt(payload.user_profile)
    
    # Construct message array
    messages =[{"role": "system", "content": system_prompt}]
    for msg in payload.chat_history:
        messages.append({"role": msg.role, "content": msg.content})
    
    messages.append({"role": "user", "content": payload.message})
    
    # Call OpenAI
    reply = await generate_chat_response(messages)
    
    return ChatResponse(reply=reply)