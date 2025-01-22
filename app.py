import os
from urllib.parse import unquote
from flask import Flask, render_template, request, redirect, url_for, flash, session
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default-secret-key')  # Added default key for development

# Use absolute path for py.txt
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUIZ_FILE = os.path.join(BASE_DIR, "py.txt")

def load_quiz(file_name):
    quiz_data = {}
    with open(file_name, "r", encoding="utf-8") as file:
        lines = file.readlines()
        current_category = None
        current_question = None
        current_options = []
        correct_answer = None
        question_id = 0  # Added to track question IDs

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Identify category
            if line.startswith("#"):
                if current_category and current_question:
                    # Save the previous question to the current category
                    quiz_data[current_category].append({
                        "id": question_id,  # Added question ID
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
                        "id": question_id,  # Added question ID
                        "question": current_question,
                        "options": current_options,
                        "correct": correct_answer
                    })
                    question_id += 1  # Increment question ID
                current_question = line[1:].strip()
                current_options = []
                correct_answer = None

            # Identify correct and incorrect options
            elif line.startswith("$"):
                correct_answer = line[1:].strip()
                current_options.append(correct_answer)
            elif line.startswith("&"):
                current_options.append(line[1:].strip())

        # Save the last question in the file
        if current_category and current_question:
            quiz_data[current_category].append({
                "id": question_id,  # Added question ID
                "question": current_question,
                "options": current_options,
                "correct": correct_answer
            })

    return quiz_data

# Load quiz data
quiz_data = load_quiz(QUIZ_FILE)

# After loading quiz data
app.logger.info(f"Loaded categories: {list(quiz_data.keys())}")

@app.route("/")
def index():
    categories = list(quiz_data.keys())
    return render_template("index.html", categories=categories)

@app.route("/quiz/<category>", methods=["GET", "POST"])
def quiz(category):
    category = unquote(category)
    if category not in quiz_data:
        flash("Category not found!", "error")
        return redirect(url_for("index"))

    questions = quiz_data[category]
    
    if request.method == "POST":
        user_answers = request.form.to_dict()
        score = 0
        total = len(questions)
        results = []

        for question in questions:
            question_id = str(question["id"])
            user_answer = user_answers.get(f"q{question_id}")
            is_correct = user_answer == question["correct"]

            results.append({
                "question": question["question"],
                "user_answer": user_answer,
                "correct_answer": question["correct"],
                "is_correct": is_correct
            })

            if is_correct:
                score += 1

        return render_template(
            "result.html",
            score=score,
            total=total,
            category=category,
            results=results
        )

    return render_template("quiz.html", category=category, questions=questions)


@app.route("/review_last_quiz")
def review_last_quiz():
    results = session.get('last_quiz_results')
    if not results:
        flash("No quiz results found!", "error")
        return redirect(url_for("index"))
    return render_template("review.html", **results)

if __name__ == "__main__":
    app.run(debug=True)