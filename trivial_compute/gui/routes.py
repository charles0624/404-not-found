from flask import Blueprint, render_template, request, jsonify

from databased.models.Question import Question
from databased.models.Category import Category
from databased.models.DeckTag import DeckTag

from databased.db import db

gui_blueprint = Blueprint("gui_blueprint", __name__, template_folder="templates")


@gui_blueprint.route("/")
def index():
    return render_template("index.html")


@gui_blueprint.route("/create_question", methods=["GET"])
def create_question():
    return render_template("create_question.html")


# this function is performed when a player clicks "submit" on 'create_question.html'
@gui_blueprint.route("/submit_question", methods=["POST"])
def submit_question():
    question = request.form["question"]
    answer = request.form["answer"]
    category = request.form["category"]
    deck_tags = request.form["deck_tags"]

    # 1. Find or create category
    table_category = (
        db.session.query(Category).filter(Category.name == category).first()
    )
    if not table_category:
        table_category = Category(name=category)
        db.session.add(table_category)
        db.session.flush()  # ensure category.id is available for FK

    # 2. Create the Question object, assign by FK directly
    table_question = Question(
        question_text=question,
        answer_text=answer,
        category_id=table_category.id,  # avoids relationship warnings
    )
    db.session.add(table_question)
    db.session.flush()  # get question.id if needed later

    # 3. Handle deck tags (many-to-many)
    # for tag_name in data.get('deck_tags', []):
    for tag_name in deck_tags:
        tag = db.session.query(DeckTag).filter(DeckTag.name == tag_name).first()
        if not tag:
            tag = DeckTag(name=tag_name)
            db.session.add(tag)
            db.session.flush()
        table_question.deck_tags.append(tag)

    db.session.commit()

    response_msg = "question commited!"
    return render_template("create_question.html", response_message=response_msg)


@gui_blueprint.route("/questions", methods=["GET"])
def list_questions():
    questions = db.session.query(Question).all()
    return render_template("all_questions.html", questions=questions)


@gui_blueprint.route("/update_question/<int:question_id>", methods=["GET"])
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
    return render_template("question_data")


@gui_blueprint.route("/questions/<int:question_id>", methods=["DELETE"])
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return render_template("")
