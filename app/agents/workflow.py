from langgraph.graph import StateGraph, END
from typing import Dict, List
from app.agents.nodes import generate_titles, generate_details, verify_stories

class GraphState(Dict):
    epic: str
    story_titles: List[str]
    stories: List[Dict]

def create_workflow():
    workflow = StateGraph(GraphState)

    workflow.add_node("generate_titles", generate_titles)
    workflow.add_node("generate_details", generate_details)
    workflow.add_node("verify_stories", verify_stories)

    workflow.set_entry_point("generate_titles")
    workflow.add_edge("generate_titles", "generate_details")
    workflow.add_edge("generate_details", "verify_stories")
    workflow.add_edge("verify_stories", END)

    return workflow.compile()