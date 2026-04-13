from fastapi import APIRouter
from app.models.requests import DashboardDataRequest # Re-use for input
from app.models.responses import SoundTherapyRecommendationResponse
from app.services.openai_client import generate_json_response
from app.prompts.recommendation_prompts import get_sound_therapy_recommendation_prompt

router = APIRouter()

# In a real app, this list would be fetched from your main backend's database.
# For this example, we'll hardcode it so the AI knows what tracks exist.
AVAILABLE_TRACKS_LIBRARY = [
    {"id": "sound_001", "title": "Ivorian Rainforest", "category": "sleep"},
    {"id": "sound_002", "title": "Grand-Bassam Waves", "category": "relaxation"},
    {"id": "sound_003", "title": "Deep Concentration", "category": "focus"},
    {"id": "sound_004", "title": "African Night", "category": "sleep"},
    {"id": "sound_005", "title": "Guided Meditation", "category": "relaxation"},
    {"id": "sound_006", "title": "Energizing Wake-up", "category": "focus"},
    {"id": "sound_007", "title": "Deep Sleep", "category": "sleep"}
]

@router.post("/sound-therapy", response_model=SoundTherapyRecommendationResponse)
async def get_sound_therapy_recommendation(payload: DashboardDataRequest):
    system_prompt = get_sound_therapy_recommendation_prompt(payload.user_profile.language)

    # We must provide the AI with BOTH the user's data and the list of available tracks.
    user_context = f"""
    Analyze the following User Data and choose the best tracks from the Available Tracks list.
    ---
    User Data:
    {payload.daily_health_data.model_dump_json()}
    ---
    Available Tracks:
    {str(AVAILABLE_TRACKS_LIBRARY)}
    ---
    """

    result_dict = await generate_json_response(system_prompt, user_context)

    return SoundTherapyRecommendationResponse(**result_dict)