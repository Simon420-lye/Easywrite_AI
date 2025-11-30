# rewrite_api.py
from dotenv import load_dotenv
import os
import time
from groq import Groq
from plagiarism_check import check_plagiarism
from ai_detect import detect_ai

load_dotenv()
GROQ_KEY = os.getenv("GROQ_KEY")

if not GROQ_KEY:
    raise RuntimeError("Set GROQ_KEY in your environment before running.")

client = Groq(api_key=GROQ_KEY)
MODEL = "llama-3.3-70b-versatile"

MAX_ATTEMPTS = 3  # Max retries for generating fully clean text

def rewrite_text(text: str, style: str = None) -> str:
    """
    Rewrite text to be fully human-like, plagiarism-free, and low AI-detection.
    style: optional string like "formal", "casual", "academic"
    """
    style_note = f" Write in a {style} tone." if style else ""
    
    for attempt in range(MAX_ATTEMPTS):
        # Step 1: Generate rewritten text
        prompt = (
            "You are a real university student writing an assignment. Rewrite the following text naturaly so it is:\n"
            "- Make it readable, human-like, and engaging..\n"
            "- Completely plagiarism-free.\n"
            "- Use varied sentence length.\n"
            "- Cannot be detected as AI-generated.\n"
            "- Keep meaning exactly the same.\n"
            "- Preserves all original meaning.\n"
            "- Avoid formal AI patterns.\n"
            "- Do not add new facts. \n"
            "- Keep plagiarism <10%.\n"
            "- Aim for AI detection <10%.\n"
            "- Written in proper academic English suitable for bachelor-level assignments.\n"
            f"{style_note}\n\n"
            f"Original Text:\n{text}\n\n"
            "Output ONLY the rewritten text."
        )
        
        try:
            resp = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.75,
                max_tokens=500
            )
            rewritten = resp.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating text: {e}"
        
        # Step 2: Check plagiarism
        plagiarism_result = check_plagiarism(rewritten)
        similarity_score = plagiarism_result.get("similarity_score", 0)

        # Step 3: Check AI detection
        ai_result = detect_ai(rewritten)
        ai_score = ai_result.get("ai_score", 0)

        # Step 4: If both are low enough, return
        if similarity_score < 10 and ai_score < 10:  # thresholds can be tuned
            return rewritten
        
        # Step 5: If not, try again with feedback
        feedback = (
            f"The last generated text had {similarity_score}% plagiarism "
            f"and {ai_score}% AI-detection. Rewrite more naturally and human-like."
        )
        prompt += "\n\n" + feedback
        time.sleep(1)  # small pause before retry
    
    # Step 6: If all attempts fail, return best effort
    return rewritten + "\n\n(Note: System tried to optimize human-likeness and plagiarism, but may need manual review.)"
