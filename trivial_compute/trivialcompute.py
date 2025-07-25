from flask import Flask, render_template, request, jsonify
from models import db, Question, Category, DeckTag

from pathlib import Path

# name the app as the parent dir
APP_NAME = Path(__file__).stem
print(f"APP_NAME: {APP_NAME}")
app = Flask(APP_NAME)

# name the database as parentdir.db
APP_DB = f"{Path.cwd()}/databased/{APP_NAME}.db"
print(f"APP DATABASE: {APP_DB}")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{APP_DB}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# call this function when cleaning up
# app.teardown_appcontext(close_db)

db.init_app(app)


@app.before_request
def create_tables():
    db.create_all()


@app.route("/")
def index():
    # return "Question DB is ready!"
    return render_template("index.html")


@app.route("/questions", methods=["POST"])
def create_question():
    data = request.json

    # 1. Find or create category
    category = Category.query.filter_by(name=data["category"]).first()
    if not category:
        category = Category(name=data["category"])
        db.session.add(category)
        db.session.flush()  # ensure category.id is available for FK

    # 2. Create the Question object, assign by FK directly
    question = Question(
        question_text=data["question"],
        answer_text=data["answer"],
        category_id=category.id,  # avoids relationship warnings
    )
    db.session.add(question)
    db.session.flush()  # get question.id if needed later

    # 3. Handle deck tags (many-to-many)
    for tag_name in data.get("deck_tags", []):
        tag = DeckTag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = DeckTag(name=tag_name)
            db.session.add(tag)
            db.session.flush()
        question.deck_tags.append(tag)

    db.session.commit()

    # return jsonify({"message": "Question added", "id": question.id})
    return render_template("create_question")


@app.route("/questions/<int:question_id>", methods=["GET"])
def get_question(question_id):
    question = Question.query.get_or_404(question_id)
    return jsonify(
        {
            "id": question.id,
            "question": question.question_text,
            "answer": question.answer_text,
            "category": question.category.name,
            "deck_tags": [tag.name for tag in question.deck_tags],
        }
    )


@app.route("/questions", methods=["GET"])
def list_questions():
    questions = Question.query.all()
    # return jsonify([
    #    {
    #        "id": q.id,
    #        "question": q.question_text,
    #        "answer": q.answer_text,
    #        "category": q.category.name,
    #        "deck_tags": [tag.name for tag in q.deck_tags]
    #    }
    #    for q in questions
    # ])
    return render_template("all_questions.html", questions=questions)


@app.route("/questions/<int:question_id>", methods=["PUT"])
def update_question(question_id):
    question = Question.query.get_or_404(question_id)
    data = request.json

    if "question" in data:
        question.question_text = data["question"]
    if "answer" in data:
        question.answer_text = data["answer"]
    if "category" in data:
        category = Category.query.filter_by(name=data["category"]).first()
        if not category:
            category = Category(name=data["category"])
            db.session.add(category)
        question.category = category
    if "deck_tags" in data:
        question.deck_tags.clear()
        for tag_name in data["deck_tags"]:
            tag = DeckTag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = DeckTag(name=tag_name)
            question.deck_tags.append(tag)

    db.session.commit()
    return jsonify({"message": "Question updated", "id": question.id})


@app.route("/questions/<int:question_id>", methods=["DELETE"])
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return jsonify({"message": "Question deleted"})


if __name__ == "__main__":
    app.run(debug=True)
