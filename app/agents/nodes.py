from langchain_openai import ChatOpenAI
from typing import Dict, List
from app.models.schemas import StoryResponse
from app.core.config import settings
import json
import re

async def generate_titles(state: Dict):
    epic = state["epic"]
    model = ChatOpenAI(model=settings.MODEL_NAME, temperature=0.2, api_key=settings.OPENAI_API_KEY, timeout=30,            # abort calls taking >30 seconds
    max_retries=1)
    prompt = f"""
You are an expert in product backlog refinement. Given the following epic, generate a list of user story titles that decompose the epic into manageable parts.
You have to generate maxiumum of 3 titles.
Epic:
"{epic}"

Return the titles in a JSON array of strings.
"""
    response = await model.ainvoke(prompt)
    content = response.content.strip()
    if content.startswith("```"):
        content = re.sub(r"^```[a-zA-Z]*\n?", "", content)
        content = re.sub(r"\n?```$", "", content)
    titles = json.loads(content)
    print(f"Titles generated: \n{titles}")
    return {"story_titles": titles}

async def generate_details(state: Dict):
    titles = state["story_titles"]
    stories = []
    model = ChatOpenAI(model=settings.MODEL_NAME, temperature=0.2, api_key=settings.OPENAI_API_KEY, timeout=30,            # abort calls taking >30 seconds
    max_retries=1)
    for title in titles:
        prompt = f"""
For the given user story title, generate a detailed description and acceptance criteria.

Story Title:
"{title}"

The description should include:
- API endpoints (e.g., POST /api/users)
- Request/response format
- Error handling (e.g., 400, 401, 500)
- Validation rules
- Security considerations

Acceptance criteria should be specific, measurable, and testable.

Return a JSON object with keys:
- "story_description"
- "story_acceptance_criteria"
"""
        response = await model.ainvoke(prompt)
        content = response.content.strip()
        if content.startswith("```"):
            content = re.sub(r"^```[a-zA-Z]*\n?", "", content)
            content = re.sub(r"\n?```$", "", content)
        story = json.loads(content)
        story["story_title"] = title
        # Ensure both fields are strings
        if isinstance(story.get("story_description"), (dict, list)):
            story["story_description"] = json.dumps(story["story_description"], ensure_ascii=False, indent=2)
        if isinstance(story.get("story_acceptance_criteria"), (dict, list)):
            story["story_acceptance_criteria"] = json.dumps(story["story_acceptance_criteria"], ensure_ascii=False, indent=2)
        stories.append(story)
    print(f"Stories generated: \n{stories}")
    return {"stories": stories}

async def verify_stories(state: Dict):
    stories = state["stories"]
    verified_stories = []
    model = ChatOpenAI(model=settings.MODEL_NAME, temperature=0.1, api_key=settings.OPENAI_API_KEY, timeout=30,            # abort calls taking >30 seconds
    max_retries=1)
    for story in stories:
        prompt = f"""
Review the following user story for completeness:
{story}

Ensure that:
- The story includes API endpoints, request/response parameters
- Error scenarios with corresponding HTTP status codes are described
- Validation rules and security constraints are included
- Acceptance criteria cover both success and failure cases

Return a JSON object with:
- "complete" (boolean)
- "feedback" (string) if incomplete
"""
        response = await model.ainvoke(prompt)
        content = response.content.strip()
        if content.startswith("```"):
            content = re.sub(r"^```[a-zA-Z]*\n?", "", content)
            content = re.sub(r"\n?```$", "", content)
        result = json.loads(content)
        if result["complete"]:
            # Ensure both fields are strings
            if isinstance(story.get("story_description"), (dict, list)):
                story["story_description"] = json.dumps(story["story_description"], ensure_ascii=False, indent=2)
            if isinstance(story.get("story_acceptance_criteria"), (dict, list)):
                story["story_acceptance_criteria"] = json.dumps(story["story_acceptance_criteria"], ensure_ascii=False, indent=2)
            verified_stories.append(story)
    print(f"Verified stories: \n{verified_stories}")
    return {"stories": verified_stories}