from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def load_quiz(file_name="py.txt"):
    quiz_data = {}
    with open(file_name, "r") as file:
        lines = file.readlines()
        current_category = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):  # Category starts with #
                current_category = line[1:].strip()  # Remove # and whitespace
                quiz_data[current_category] = []
            elif line.startswith("*") and current_category:  # Questions start with *
                question = line[1:].strip()  # Remove * and whitespace
                quiz_data[current_category].append(question)
    return quiz_data

# Load questions from the text file
quiz_data = load_quiz("py.txt")

@app.route("/")
def index():
    categories = list(quiz_data.keys())  # Get all categories
    return render_template("index.html", categories=categories)

@app.route("/quiz/<category>", methods=["GET", "POST"])
def quiz(category):
    if category not in quiz_data:
        return redirect(url_for("index"))

    questions = quiz_data[category]  # Ensure this is a list
    if request.method == "POST":
        user_answers = request.form.to_dict()
        score = sum(1 for answer in user_answers.values() if answer.strip())  # Example scoring
        return render_template("result.html", score=score, total=len(questions))

    return render_template("quiz.html", category=category, questions=questions)

if __name__ == "__main__":
    app.run(debug=True)
