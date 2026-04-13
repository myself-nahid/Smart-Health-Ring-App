import json
import asyncio
from openai import AsyncOpenAI, InternalServerError, APIError, APITimeoutError
from app.core.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY, timeout=120)

async def generate_json_response(system_prompt: str, user_data: str) -> dict:
    """Generates structured JSON using OpenAI's JSON mode."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
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
        except (InternalServerError, APITimeoutError) as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"OpenAI {type(e).__name__} (attempt {attempt + 1}/{max_retries}): {e}. Retrying in {wait_time}s...")
                await asyncio.sleep(wait_time)
            else:
                print(f"OpenAI {type(e).__name__} after {max_retries} attempts: {e}")
                raise
        except APIError as e:
            print(f"OpenAI API Error: {e}")
            raise

async def generate_chat_response(messages: list) -> str:
    """Standard text chat generation for AI Doctor Simbi."""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = await client.chat.completions.create(
                model=settings.MODEL_NAME,
                messages=messages,
                temperature=0.7
            )
            return response.choices[0].message.content
        except (InternalServerError, APITimeoutError) as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"OpenAI {type(e).__name__} (attempt {attempt + 1}/{max_retries}): {e}. Retrying in {wait_time}s...")
                await asyncio.sleep(wait_time)
            else:
                print(f"OpenAI {type(e).__name__} after {max_retries} attempts: {e}")
                raise
        except APIError as e:
            print(f"OpenAI API Error: {e}")
            raise