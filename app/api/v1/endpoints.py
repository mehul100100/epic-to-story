from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
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
        print(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "message": str(e)
            }
        )