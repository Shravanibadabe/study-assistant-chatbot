import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise Exception("GEMINI_API_KEY is not configured.")

client = genai.Client(api_key=api_key)

SYSTEM_PROMPT = """
You are a helpful AI Study Assistant for college students.

Answer rules:
1. Keep answers short, clear, and easy for students to understand.
2. Use a suitable heading followed by short bullet points.
3. Avoid long paragraphs and unnecessary introductions.
4. For academic explanations, use this format when suitable:

   **Meaning:** One or two simple sentences.

   **Key Points:**
   - Point 1
   - Point 2
   - Point 3

   **Example:** Give one short example if useful.

5. Keep the answer around 80-120 words unless the student asks for
   a detailed or exam-oriented answer.
6. For simple questions, answer directly without forcing every section.
7. Do not repeat the question or add unrelated information.
8. If the question is unclear, ask one brief clarification question.
"""

def ask_gemini(question):
    prompt = f"""
{SYSTEM_PROMPT}

Student's question:
{question}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        if response.text:
            return response.text.strip()

        return "I couldn't generate a response. Please try asking another way."

    except Exception as e:
        print("Gemini error:", e)
        return "The AI service is temporarily unavailable. Please try again."