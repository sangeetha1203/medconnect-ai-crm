from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY

def followup_recommendation_tool(notes: str):
    try:
        llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name="llama-3.3-70b-versatile",
            temperature=0
        )

        prompt = f"""
Based on this doctor interaction,
generate a smart sales follow-up recommendation.

Notes:
{notes}
"""

        response = llm.invoke(prompt)

        return {
            "ai_followup": response.content,
            "source": "groq_llm"
        }

    except Exception:
        return {
            "ai_followup": "Schedule follow-up within 3 days",
            "source": "fallback"
        }