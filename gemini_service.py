import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise Exception("GEMINI_API_KEY is not configured.")

client = genai.Client(api_key=api_key)


def ask_gemini(question):
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=question
        )

        if response.text:
            return response.text

        return "I couldn't generate a response."

    except Exception as e:
        print("Gemini error:", e)
        return "Gemini is temporarily unavailable. Please try again."