from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

async def openai_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=503,
        content={"message": "AI Service is temporarily unavailable. Please try again later.", "details": str(exc)},
    )