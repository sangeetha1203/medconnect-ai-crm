from app.services.llm_service import llm

def doctor_profile_tool(text: str):
    prompt = f"""
    Extract doctor profile details from this interaction text.

    Return:
    - doctor_name
    - specialization
    - hospital
    - engagement_priority

    Interaction:
    {text}
    """

    response = llm.invoke(prompt)

    return {
        "doctor_profile": response.content,
        "source": "groq_llm"
    }