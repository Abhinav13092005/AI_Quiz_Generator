
import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


def generate_questions(topic):
    if not API_KEY:
        raise ValueError(
            "GEMINI_API_KEY nahi mili. Render Environment check karo."
        )

    client = genai.Client(
        api_key=API_KEY,
        http_options=types.HttpOptions(timeout=30000)
    )

    prompt = f"""
Create exactly 5 multiple-choice quiz questions about "{topic}".

Return ONLY a valid JSON array. No markdown or extra text.

Format:
[
  {{
    "question": "Question text",
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
- Exactly 5 questions.
- Exactly 4 options per question.
- Answer must be A, B, C, or D.
- Questions should be accurate and beginner-friendly.
- All questions must be different.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=2000,
                response_mime_type="application/json"
            )
        )

        response_text = (response.text or "").strip()
        questions = json.loads(response_text)

        if not isinstance(questions, list) or len(questions) != 5:
            raise ValueError("AI ne exactly 5 questions return nahi kiye.")

        for question in questions:
            if not isinstance(question, dict):
                raise ValueError("Question format galat hai.")

            if not all(
                key in question
                for key in ["question", "options", "answer"]
            ):
                raise ValueError("Question mein required fields missing hain.")

            if (
                not isinstance(question["options"], list)
                or len(question["options"]) != 4
            ):
                raise ValueError(
                    "Har question mein exactly 4 options hone chahiye."
                )

            if question["answer"] not in ["A", "B", "C", "D"]:
                raise ValueError("Correct answer A, B, C, ya D hona chahiye.")

        return questions

    except Exception as error:
        print(f"Gemini Quiz Generation Error: {type(error).__name__}: {error}")
        raise
