from app.agents.workflow import create_workflow
from app.models.schemas import StoryGenerationResponse
import json

async def generate_stories_from_epic(epic: str):
    workflow = create_workflow()
    print(f"Started Workflow")
    result = await workflow.ainvoke({"epic": epic})
    print(f"Workflow completed")
    stories = result.get("stories", [])
    return StoryGenerationResponse(stories=stories)