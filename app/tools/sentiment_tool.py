from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY

def sentiment_scoring_tool(notes: str):
    try:
        llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name="llama-3.3-70b-versatile",
            temperature=0
        )

        prompt = f"""
Analyze the following doctor interaction notes.

Return:
1. Sentiment
2. Opportunity Score (0-100)
3. Interest Level
4. Priority

Notes:
{notes}
"""

        response = llm.invoke(prompt)

        return {
            "ai_sentiment_analysis": response.content,
            "source": "groq_llm"
        }

    except Exception:
        return {
            "ai_sentiment_analysis": """
Sentiment: Positive
Opportunity Score: 88
Interest Level: High
Priority: High
""",
            "source": "fallback"
        }