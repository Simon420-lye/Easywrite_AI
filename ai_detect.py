# ai_detect.py
from dotenv import load_dotenv
import os
import json
from groq import Groq

load_dotenv()
GROQ_KEY = os.getenv("GROQ_KEY")

if not GROQ_KEY:
    raise RuntimeError("Set GROQ_KEY in your environment.")

client = Groq(api_key=GROQ_KEY)

MODEL = "llama-3.3-70b-versatile"


def detect_ai(text: str) -> dict:
    """
    Returns JSON in this EXACT structure (required by UI):

    {
        "ai_detection": {
            "ai_score": 35,
            "human_score": 65,
            "summary": "...",
            "explanation": "..."
        }
    }
    """

    prompt = f"""
You are an advanced AI-text detection engine for the brand 'roroWrites HumanAizer'.

Analyze the following text and return ONLY valid JSON in this format:

{{
 "ai_score": number (0–100),
 "human_score": number (0–100),
 "summary": "short human-readable conclusion (1–2 sentences)",
 "explanation": "detailed reasoning"
}}

Text to analyze:
{text}
"""

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=300
        )

        raw = resp.choices[0].message.content.strip()
        data = json.loads(raw)

        # Ensure all values exist
        ai_score = float(data.get("ai_score", 0))
        human_score = float(data.get("human_score", 100))
        summary = data.get("summary", "No summary.")
        explanation = data.get("explanation", "No explanation.")

        # Organize in correct UI structure
        return {
            "ai_detection": {
                "ai_score": ai_score,
                "human_score": human_score,
                "summary": summary,
                "explanation": explanation
            }
        }

    except Exception as e:
        return {"error": str(e)}
