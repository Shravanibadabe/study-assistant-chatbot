import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise Exception("GEMINI_API_KEY is not configured.")

client = genai.Client(api_key=api_key)

SYSTEM_PROMPT = """
You are a concise AI Study Assistant for college students.
Answer clearly and accurately in simple language.
Use a short heading and bullet points when useful.
Keep normal answers under 100 words.
If the student asks for a detailed or exam-oriented answer,
give the requested detail.
Do not include unnecessary introductions or repeat the question.
Return plain Markdown only. Do not wrap the answer in a code block.
"""

def ask_gemini(question):
    prompt = f"{SYSTEM_PROMPT}\n\nStudent's question: {question}"

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config={
                "max_output_tokens": 250,
                "temperature": 0.3
            }
        )

        if response.text:
            return response.text.strip()

        return "I couldn't generate a response. Please try again."

    except Exception as e:
        print("Gemini error:", e)
        return "The AI service is temporarily unavailable. Please try again."