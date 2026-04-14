from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.models.requests import ChatRequest
from app.services.openai_client import stream_simbi_response
from app.prompts.simbi_prompts import get_simbi_system_prompt
import json

router = APIRouter()

# @router.websocket("/ws")
# async def simbi_websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
    
#     try:
#         while True:
#             # 1. Receive JSON data from the mobile app
#             data = await websocket.receive_text()
#             payload_dict = json.loads(data)
            
#             # Map raw dict to our ChatRequest Pydantic model for validation
#             payload = ChatRequest(**payload_dict)
            
#             # 2. Prepare the prompt context
#             system_prompt = get_simbi_system_prompt(payload.user_profile)
#             messages = [{"role": "system", "content": system_prompt}]
#             for msg in payload.chat_history:
#                 messages.append({"role": msg.role, "content": msg.content})
#             messages.append({"role": "user", "content": payload.message})
            
#             # 3. Stream back to the client
#             # We send a "start" signal
#             await websocket.send_json({"type": "start"})
            
#             async for text_chunk in stream_simbi_response(messages):
#                 await websocket.send_json({
#                     "type": "chunk",
#                     "content": text_chunk
#                 })
            
#             # 4. Send "end" signal
#             await websocket.send_json({"type": "end"})
            
#     except WebSocketDisconnect:
#         print("Client disconnected from Simbi Chat")
#     except Exception as e:
#         print(f"WebSocket Error: {e}")
#         await websocket.send_json({"type": "error", "message": str(e)})
#         await websocket.close()


@router.websocket("/ws")
async def simbi_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            payload = ChatRequest(**json.loads(data))
            
            system_prompt = get_simbi_system_prompt(payload.user_profile)
            messages = [{"role": "system", "content": system_prompt}]
            for msg in payload.chat_history:
                messages.append({"role": msg.role, "content": msg.content})
            messages.append({"role": "user", "content": payload.message})
            
            await websocket.send_json({"type": "start"})
            
            # Variable to store the full text
            full_response_text = "" 
            
            async for text_chunk in stream_simbi_response(messages):
                full_response_text += text_chunk # Add chunk to the full string
                await websocket.send_json({
                    "type": "chunk",
                    "content": text_chunk
                })
            
            # Send the complete text as one message for easy testing 
            await websocket.send_json({
                "type": "full_text", 
                "content": full_response_text
            })
            
            await websocket.send_json({"type": "end"})
            
    except WebSocketDisconnect:
        pass

# from fastapi import APIRouter, HTTPException
# from app.models.requests import ChatRequest
# from app.models.responses import ChatResponse
# from app.services.openai_client import generate_chat_response
# from app.prompts.simbi_prompts import get_simbi_system_prompt
# from openai import APIError, APITimeoutError

# router = APIRouter()

# @router.post("/simbi-chat", response_model=ChatResponse)
# async def simbi_chat_endpoint(payload: ChatRequest):
#     try:
#         system_prompt = get_simbi_system_prompt(payload.user_profile)
        
#         # Construct message array
#         messages =[{"role": "system", "content": system_prompt}]
#         for msg in payload.chat_history:
#             messages.append({"role": msg.role, "content": msg.content})
        
#         messages.append({"role": "user", "content": payload.message})
        
#         # Call OpenAI
#         reply = await generate_chat_response(messages)
        
#         return ChatResponse(reply=reply)
#     except APITimeoutError as e:
#         raise HTTPException(status_code=504, detail=f"AI service timeout: {str(e)}")
#     except APIError as e:
#         raise HTTPException(status_code=503, detail=f"AI service temporarily unavailable: {str(e)}")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")