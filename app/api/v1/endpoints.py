from fastapi import APIRouter, HTTPException
from app.models.schemas import EpicRequest, StoryGenerationResponse
from app.services.story_generation_service import generate_stories_from_epic
import traceback

router = APIRouter(prefix="/stories", tags=["Stories"])

@router.post("/", response_model=StoryGenerationResponse)
async def generate_stories(request: EpicRequest):
    try:
        result = await generate_stories_from_epic(request.epic)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}, stacktrace: {traceback.format_exc()}")