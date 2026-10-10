
import os
from flask import Flask, request, render_template_string, session
from quiz_data import generate_questions

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "local-dev-key-change-later")

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Quiz Generator</title>
    <style>
        * { box-sizing: border-box; }

        body {
            font-family: Arial, sans-serif;
            background: #0f172a;
            color: white;
            margin: 0;
            padding: 30px 15px;
        }

        .container {
            max-width: 750px;
            margin: auto;
            background: #1e293b;
            padding: 25px;
            border-radius: 15px;
        }

        h1, h2 { color: #38bdf8; }

        input[type="text"] {
            width: 100%;
            padding: 13px;
            border-radius: 7px;
            border: none;
            margin: 10px 0;
            font-size: 16px;
        }

        button {
            padding: 12px 22px;
            background: #0284c7;
            color: white;
            border: none;
            border-radius: 7px;
            font-size: 16px;
            cursor: pointer;
        }

        button:hover { background: #0369a1; }

        .question {
            background: #334155;
            padding: 18px;
            margin: 18px 0;
            border-radius: 10px;
        }

        .option {
            display: block;
            padding: 9px 0;
            cursor: pointer;
        }

        .message {
            background: #7f1d1d;
            padding: 12px;
            border-radius: 7px;
            margin-top: 15px;
            overflow-wrap: anywhere;
        }

        .score {
            background: #164e63;
            padding: 18px;
            border-radius: 10px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>AI Quiz Generator</h1>
    <p>Enter any topic and generate a quiz using Gemini AI.</p>

    <form method="POST" action="/">
        <input
            type="text"
            name="topic"
            placeholder="Example: Python, Java, Artificial Intelligence"
            value="{{ topic }}"
            required
        >
        <button type="submit">Generate Quiz</button>
    </form>

    {% if error %}
        <div class="message">
            <strong>Error:</strong> {{ error }}
        </div>
    {% endif %}

    {% if questions %}
        <h2>Quiz Topic: {{ topic }}</h2>
        <p>Total Questions: {{ questions|length }}</p>

        <form method="POST" action="/check">
            {% for q in questions %}
                {% set question_index = loop.index0 %}
                <div class="question">
                    <p><strong>{{ loop.index }}. {{ q.question }}</strong></p>

                    {% for option in q.options %}
                        <label class="option">
                            <input
                                type="radio"
                                name="q{{ question_index }}"
                                value="{{ option[0] }}"
                                required
                            >
                            {{ option }}
                        </label>
                    {% endfor %}
                </div>
            {% endfor %}

            <button type="submit">Submit Answers</button>
        </form>
    {% endif %}

    {% if score is not none %}
        <div class="score">
            <h2>Your Score: {{ score }} / {{ total }}</h2>
            <p>Percentage: {{ percentage }}%</p>
            <p>{{ feedback }}</p>
            <a href="/" style="color:#7dd3fc;">Generate another quiz</a>
        </div>
    {% endif %}
</div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    topic = ""
    questions = []
    error = None

    if request.method == "POST":
        topic = request.form.get("topic", "").strip()

        if topic:
            try:
                questions = generate_questions(topic)
                session["quiz_questions"] = questions
                session["quiz_topic"] = topic
            except Exception as e:
                print("Quiz generation error:", repr(e))
                error = str(e)
                if not error:
                    error = "Unknown error. Terminal check karo."

    return render_template_string(
        HTML,
        topic=topic,
        questions=questions,
        error=error,
        score=None,
        total=0,
        percentage=0,
        feedback=""
    )


@app.route("/check", methods=["POST"])
def check():
    questions = session.get("quiz_questions", [])
    topic = session.get("quiz_topic", "")

    if not questions:
        return render_template_string(
            HTML,
            topic=topic,
            questions=[],
            error="Quiz session nahi mila. Pehle naya quiz generate karo.",
            score=None,
            total=0,
            percentage=0,
            feedback=""
        )

    score = 0

    for i, question in enumerate(questions):
        user_answer = request.form.get(f"q{i}", "")
        if user_answer == question["answer"]:
            score += 1

    total = len(questions)
    percentage = round((score / total) * 100, 2) if total else 0

    if percentage >= 80:
        feedback = "Excellent work!"
    elif percentage >= 50:
        feedback = "Good effort! Keep practising."
    else:
        feedback = "Keep learning and try again."

    session.pop("quiz_questions", None)
    session.pop("quiz_topic", None)

    return render_template_string(
        HTML,
        topic=topic,
        questions=[],
        error=None,
        score=score,
        total=total,
        percentage=percentage,
        feedback=feedback
    )


if __name__ == "__main__":
    app.run(debug=True)