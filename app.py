import os
from urllib.parse import unquote
from flask import Flask, render_template, request, redirect, url_for
import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


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

            # Check for a category
            if line.startswith("#"):
                if current_category:
                    # Save the last question
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

            # Check for a question
            elif line.startswith("*"):
                if current_question:
                    # Save the last question
                    quiz_data[current_category].append({
                        "question": current_question,
                        "options": current_options,
                        "correct": correct_answer
                    })
                current_question = line[1:].strip()
                current_options = []
                correct_answer = None

            # Check for answers
            elif line.startswith("$"):
                correct_answer = line[1:].strip()
                current_options.append(correct_answer)
            elif line.startswith("&"):
                current_options.append(line[1:].strip())

        # Save the last question
        if current_question:
            quiz_data[current_category].append({
                "question": current_question,
                "options": current_options,
                "correct": correct_answer
            })

    return quiz_data


# Load questions from the text file
quiz_data = load_quiz("py.txt")

@app.route("/test")
def test():
    return "Test route is working!"

@app.route("/")
def index():
    categories = list(quiz_data.keys())  # Get all categories
    return render_template("index.html", categories=categories)

@app.route("/quiz/<category>", methods=["GET", "POST"])
def quiz(category):
    logging.debug(f"Category requested: {category}")
    if category not in quiz_data:
        logging.debug("Category not found")
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
