from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class EpicRequest(BaseModel):
    epic: str

class StoryResponse(BaseModel):
    story_title: str
    story_description: str
    story_acceptance_criteria: str

class StoryGenerationResponse(BaseModel):
    stories: List[StoryResponse]

class StoryTitlesResponse(BaseModel):
    story_titles: List[str] = Field(description="List of 1 to 3 story titles for the given epic")

class StoryDetail(BaseModel):
    story_title: str = Field(description="The title of the user story")
    story_description: str = Field(description="Detailed story description")
    story_acceptance_criteria: str = Field(description="Acceptance criteria for the story")

class StoryVerification(BaseModel):
    complete: bool = Field(description="Whether the story is complete")
    feedback: str = Field(default="", description="Feedback if the story is incomplete")