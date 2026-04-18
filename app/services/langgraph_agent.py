from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional

from app.tools.log_tool import log_interaction_tool
from app.tools.sentiment_tool import sentiment_scoring_tool
from app.tools.followup_tool import followup_recommendation_tool
from app.tools.doctor_profile_tool import doctor_profile_tool
from app.tools.meeting_scheduler_tool import meeting_scheduler_tool


class AgentState(TypedDict, total=False):
    input_text: str
    edit_text: Optional[str]
    search_keyword: Optional[str]

    log_result: dict
    edit_result: dict
    search_result: dict
    sentiment_result: dict
    followup_result: dict
    doctor_profile_result: dict
    meeting_schedule_result: dict

def doctor_profile_node(state):
    result = doctor_profile_tool(state["input_text"])
    state["doctor_profile_result"] = result
    return state


def meeting_scheduler_node(state):
    result = meeting_scheduler_tool(state["input_text"])
    state["meeting_schedule_result"] = result
    return state


# TOOL 1 → LOG INTERACTION
def log_node(state):
    result = log_interaction_tool(state["input_text"])
    state["log_result"] = result
    return state


# TOOL 2 → EDIT INTERACTION
def edit_node(state):
    state["edit_result"] = {
        "status": "updated",
        "message": "Interaction data can be edited by field representative",
        "updated_text": state.get("edit_text", state["input_text"])
    }
    return state


# TOOL 3 → SEARCH INTERACTION
def search_node(state):
    keyword = state.get("search_keyword", "")

    state["search_result"] = {
        "keyword": keyword,
        "status": "matched",
        "message": f"Search completed for keyword: {keyword}"
    }
    return state


# TOOL 4 → OPPORTUNITY / SENTIMENT SCORING
def sentiment_node(state):
    result = sentiment_scoring_tool(state["input_text"])
    state["sentiment_result"] = result
    return state


# TOOL 5 → FOLLOW-UP PLANNER
def followup_node(state):
    result = followup_recommendation_tool(state["input_text"])
    state["followup_result"] = result
    return state


# BUILD LANGGRAPH FLOW
builder = StateGraph(AgentState)

builder.add_node("log", log_node)
builder.add_node("edit", edit_node)
builder.add_node("search", search_node)
builder.add_node("sentiment", sentiment_node)
builder.add_node("followup", followup_node)
builder.add_node("doctor_profile", doctor_profile_node)
builder.add_node("meeting_scheduler", meeting_scheduler_node)

builder.set_entry_point("log")

builder.add_edge("log", "edit")
builder.add_edge("edit", "search")
builder.add_edge("search", "sentiment")
builder.add_edge("sentiment", "followup")
builder.add_edge("followup", END)
builder.add_edge("doctor_profile", "meeting_scheduler")
builder.add_edge("meeting_scheduler", END)

graph = builder.compile()