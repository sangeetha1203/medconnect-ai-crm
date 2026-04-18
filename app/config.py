import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

print("GROQ KEY LOADED:", GROQ_API_KEY[:10] if GROQ_API_KEY else "NOT FOUND")