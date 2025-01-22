import os
from urllib.parse import unquote
from flask import Flask, render_template, request, redirect, url_for, flash
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # needed for flash messages

# Use absolute path for py.txt
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUIZ_FILE = os.path.join(BASE_DIR, "py.txt")

def load_quiz(file_name="py.txt"):
    quiz_data = {}
    with open(file_name, "r", encoding="utf-8") as file:
        lines = file.readlines()
        current_category = None
        current_question = None
        current_options = []
        correct_answer = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Identify category
            if line.startswith("#"):
                if current_category and current_question:
                    # Save the previous question to the current category
                    quiz_data[current_category].append({
                        "question": current_question,
                        "options": current_options,
                        "correct": correct_answer
                    })
                current_category = line[1:].strip()
                quiz_data[current_category] = []
                current_question = None
                current_options = []
                correct_answer = None

            # Identify question
            elif line.startswith("*"):
                if current_question:
                    # Save the current question
                    quiz_data[current_category].append({
                        "question": current_question,
                        "options": current_options,
                        "correct": correct_answer
                    })
                current_question = line[1:].strip()
                current_options = []
                correct_answer = None

            # Identify correct and incorrect options
            elif line.startswith("$"):
                correct_answer = line[1:].strip()
                current_options.append(correct_answer)  # Mark as correct
            elif line.startswith("&"):
                current_options.append(line[1:].strip())  # Add incorrect option

        # Save the last question in the file
        if current_category and current_question:
            quiz_data[current_category].append({
                "question": current_question,
                "options": current_options,
                "correct": correct_answer
            })

    return quiz_data


@app.route("/test")
def test():
    return "Test route is working!"

# Load quiz data
quiz_data = load_quiz(QUIZ_FILE)

@app.route("/")
def index():
    categories = list(quiz_data.keys())  # Get the list of categories directly
    return render_template("index.html", categories=categories)


@app.route("/quiz/<category>", methods=["GET", "POST"])
def quiz(category):
    category = unquote(category)  # Decode URL-encoded category
    if category not in quiz_data:
        app.logger.info(f"Category not found: {category}")
        return redirect(url_for("index"))

    questions = quiz_data[category]
    if request.method == "POST":
        user_answers = request.form.to_dict()
        score = 0
        total = len(questions)

        # Calculate the score
        for idx, question in enumerate(questions, start=1):
            user_answer = user_answers.get(f"q{idx}")
            if user_answer == question["correct"]:
                score += 1

        return render_template("result.html", score=score, total=total)

    return render_template("quiz.html", category=category, questions=questions)

if __name__ == "__main__":
    app.run(debug=True)
