from gemini_service import ask_gemini


question = "Explain machine learning to a beginner in simple words."

answer = ask_gemini(question)

print(answer)