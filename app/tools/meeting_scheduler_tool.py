from app.services.llm_service import llm

def meeting_scheduler_tool(text: str):
    prompt = f"""
    Analyze this doctor interaction and suggest:

    - next meeting date
    - follow-up action
    - reminder priority

    Interaction:
    {text}
    """

    response = llm.invoke(prompt)

    return {
        "meeting_schedule": response.content,
        "source": "groq_llm"
    }