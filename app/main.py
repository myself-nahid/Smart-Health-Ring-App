from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import chat, insights, prediction, dashboard
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Stateless AI processing engine for BISO Health Ring",
    version="1.0.0"
)

# CORS middleware to allow main backend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, change to the actual IP/Domain of your Django/Node backend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(chat.router, prefix="/api/v1/chat", tags=["AI Doctor Simbi"])
app.include_router(insights.router, prefix="/api/v1/insights", tags=["Health Insights"])
app.include_router(prediction.router, prefix="/api/v1/prediction", tags=["Risk Prediction"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard Generation"])

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok", "service": settings.PROJECT_NAME}

# If running locally without Docker:
# run: uvicorn app.main:app --reload