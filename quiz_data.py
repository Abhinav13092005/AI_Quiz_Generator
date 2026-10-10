
import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


def generate_questions(topic):
    if not API_KEY:
        raise ValueError(
            "GEMINI_API_KEY nahi mili. Apni .env file check karo."
        )

    client = genai.Client(api_key=API_KEY)

    prompt = f"""
Create exactly 5 multiple-choice quiz questions about "{topic}".

Return ONLY a valid JSON array. Do not include markdown or extra text.

Use exactly this format:
[
  {{
    "question": "Question 1",
    "options": [
      "A. First option",
      "B. Second option",
      "C. Third option",
      "D. Fourth option"
    ],
    "answer": "A"
  }}
]

Rules:
- Return exactly 5 question objects.
- Each question must have exactly 4 options.
- Every option must start with A., B., C., or D.
- The answer must be only A, B, C, or D.
- Make questions accurate and beginner-friendly.
- Make all five questions different.
"""

    response = client.models.generate_content(
    model="gemini-3.7-flash",
        contents=prompt
    )

    response_text = (response.text or "").strip()
    response_text = response_text.replace("```json", "").replace("```", "").strip()

    questions = json.loads(response_text)

    if not isinstance(questions, list) or len(questions) != 5:
        raise ValueError("AI ne exactly 5 questions return nahi kiye.")

    for question in questions:
        if not isinstance(question, dict):
            raise ValueError("Question format galat hai.")

        if not all(key in question for key in ["question", "options", "answer"]):
            raise ValueError("Question mein required fields missing hain.")

        if not isinstance(question["options"], list) or len(question["options"]) != 4:
            raise ValueError("Har question mein exactly 4 options hone chahiye.")

        if question["answer"] not in ["A", "B", "C", "D"]:
            raise ValueError("Correct answer A, B, C, ya D hona chahiye.")

    return questions
