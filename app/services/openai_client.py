import json
from openai import AsyncOpenAI
from app.core.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY, timeout=60)

async def generate_json_response(system_prompt: str, user_data: str) -> dict:
    """Generates structured JSON using OpenAI's JSON mode."""
    response = await client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_data}
        ],
        response_format={"type": "json_object"},
        temperature=0.4
    )
    return json.loads(response.choices[0].message.content)

async def generate_chat_response(messages: list) -> str:
    """Standard text chat generation for AI Doctor Simbi."""
    response = await client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content