from flask import Blueprint, render_template, request, jsonify

from databased.models.Question import Question
from databased.models.Category import Category
from databased.models.DeckTag import DeckTag

from databased.db import db

gui_blueprint = Blueprint("gui_blueprint", __name__, template_folder="templates")

@gui_blueprint.route("/")
def index():
    # return "Question DB is ready!"
    return render_template("index.html")


@gui_blueprint.route("/create_question", methods=["GET"])
def create_question():
    return render_template("create_question.html")

@gui_blueprint.route("/questions", methods=["GET"])
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


@gui_blueprint.route("/questions/<int:question_id>", methods=["GET"])
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
