# plagiarism_check.py
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


def check_plagiarism(user_text: str, reference_text: str = None) -> dict:
    """
    If reference_text is provided → compare similarity.
    If not provided → check if text looks copied from the internet.
    Returns dict {similarity_score, explanation}
    """

    if reference_text:
        task = f"""
You MUST return valid JSON ONLY. No explanation outside JSON.

Compare these two texts and return JSON structured like:
{{
  "similarity_score": number,
  "explanation": "string"
}}

TEXT1:
{user_text}

TEXT2:
{reference_text}
"""
    else:
        task = f"""
You MUST return valid JSON ONLY. No explanation outside JSON.

Analyze plagiarism likelihood and return JSON:
{{
  "similarity_score": number,
  "explanation": "string"
}}

TEXT:
{user_text}
"""

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": task}],
            temperature=0.1,
            max_tokens=300
        )

        raw = resp.choices[0].message.content.strip()

        # Extract only the JSON part
        json_start = raw.find("{")
        json_end = raw.rfind("}") + 1
        json_text = raw[json_start:json_end]

        return json.loads(json_text)

    except Exception as e:
        return {"error": str(e)}
