from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from typing import Dict, List
from app.models.schemas import StoryTitlesResponse, StoryDetail, StoryVerification
from app.core.config import settings

async def generate_titles(state: Dict):
    epic = state["epic"]
    model = ChatOpenAI(
        model=settings.MODEL_NAME,
        temperature=0.2,
        api_key=settings.OPENAI_API_KEY,
        timeout=30,
        max_retries=1
    )

    parser = JsonOutputParser(pydantic_object=StoryTitlesResponse)

    prompt = PromptTemplate(
        template=(
            "You are an expert in product backlog refinement. "
            "Given the following epic, generate a list of user story titles (max 3) that decompose the epic into manageable parts.\n\n"
            "{format_instructions}\n\nEpic:\n\"{epic}\""
        ),
        input_variables=["epic"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | model | parser
    result = await chain.ainvoke({"epic": epic})
    print(f"Titles generated: \n{result}")
    return result

async def generate_details(state: Dict):
    titles = state["story_titles"]
    stories = []

    model = ChatOpenAI(
        model=settings.MODEL_NAME,
        temperature=0.2,
        api_key=settings.OPENAI_API_KEY,
        timeout=30,
        max_retries=1
    )

    for title in titles:
        parser = JsonOutputParser(pydantic_object=StoryDetail)

        prompt = PromptTemplate(
            template=(
                "For the given user story title, generate a detailed description and acceptance criteria.\n\n"
                "Story Title:\n\"{title}\"\n\n"
                "The description should include:\n"
                "- API endpoints (e.g., POST /api/users)\n"
                "- Request/response format\n"
                "- Error handling (e.g., 400, 401, 500)\n"
                "- Validation rules\n"
                "- Security considerations\n\n"
                "Acceptance criteria should be specific, measurable, and testable.\n\n"
                "{format_instructions}"
            ),
            input_variables=["title"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | model | parser
        story = await chain.ainvoke({"title": title})
        stories.append(story)

    print(f"Stories generated: \n{stories}")
    return {"stories": stories}

async def verify_stories(state: Dict):
    stories = state["stories"]
    verified_stories = []

    model = ChatOpenAI(
        model=settings.MODEL_NAME,
        temperature=0.1,
        api_key=settings.OPENAI_API_KEY,
        timeout=30,
        max_retries=1
    )

    for story in stories:
        parser = JsonOutputParser(pydantic_object=StoryVerification)

        prompt = PromptTemplate(
            template=(
                "Review the following user story for completeness:\n\n"
                "{story}\n\n"
                "Ensure that:\n"
                "- The story includes API endpoints, request/response parameters\n"
                "- Error scenarios with corresponding HTTP status codes are described\n"
                "- Validation rules and security constraints are included\n"
                "- Acceptance criteria cover both success and failure cases\n\n"
                "{format_instructions}"
            ),
            input_variables=["story"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | model | parser
        result = await chain.ainvoke({"story": story})

        if "complete" in result and result["complete"]:
            verified_stories.append(story)

    print(f"Verified stories: \n{verified_stories}")
    return {"stories": verified_stories}