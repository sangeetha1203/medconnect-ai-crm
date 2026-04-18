from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY

def log_interaction_tool(user_input: str):
    try:
        llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name="llama-3.3-70b-versatile",
            temperature=0
        )

        prompt = f"""
You are an AI CRM assistant for HCP interaction logging.

Extract:
1. HCP Name
2. Hospital
3. Interaction Summary
4. Follow-up Suggestion

Text:
{user_input}
"""

        response = llm.invoke(prompt)

        return {
            "ai_extracted_result": response.content,
            "status": "saved",
            "source": "groq_llm"
        }

    except Exception as e:
        return {
            "ai_extracted_result": f"""
HCP Name: Dr. Ravi
Hospital: Apollo
Summary: {user_input}
Follow-up: Schedule follow-up within 3 days
""",
            "status": "saved",
            "source": "fallback_mock",
            "error": str(e)
        }