# web server and database stuff
from flask import Flask, redirect, render_template, request, jsonify, url_for
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
import random
import sys


from models import db, Category, DeckTag, Question
from game_object import COLORS, get_player

# name the app as the parent dir
APP_NAME = Path(__file__).stem
print(f"APP_NAME: {APP_NAME}")
app = Flask(APP_NAME)

APP_DB = f"sqlite:///{Path.cwd()}/database.db"
print(f"APP DATABASE: {APP_DB}")
app.config["SQLALCHEMY_DATABASE_URI"] = APP_DB
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# create database
db.init_app(app)
with app.app_context():
    try:
        db.create_all()
    except:
        print("OH GOD WE DIDNT CREATE THE TABLE!!!!")
        sys.exit()


HOME_PAGE = "index.html"
USERS_MENU = "users_menu.html"
GAME_SESSION = "game_session.html"

QUESTIONS_MENU = "questions_menu.html"
CREATE_QUESTION = "create_question.html"
READ_QUESTIONS = "questions.html"
UPDATE_QUESTION = "update_question.html"
DELETE_QUESTION = "delete_question.html"


###
#  Gameplay Routes
###
@app.route("/", methods=["GET"])
def index():
    return render_template(HOME_PAGE)


@app.route("/exit", methods=["GET"])
def exit():
    sys.exit()  # can't imagine this is recommended

# enter player data
@app.route("/play_game", methods=["GET"])
def play_game():
    return render_template(USERS_MENU)

def random_color_index(modulo_number):
    return random.randint(0,100) % modulo_number # ensure it is random AND between length of list, inclusive

# called from USERS_MENU
@app.route("/game_session", methods=["POST"])
def display_board():
    player_list = [
        request.form.get("player1", None),
        request.form.get("player2", None),
        request.form.get("player3", None),
        request.form.get("player4", None)
    ]
    player_colors = COLORS
    list_len = len(player_colors)
    data: dict = {}
    for player in player_list:
        player_color = player_colors.pop(random_color_index(list_len))
        data[player] = player_color
        list_len -= 1

    return render_template(GAME_SESSION, players=data)

# TODO
# @app.route("settings", methods=["GET"])
# def settings():
#    pass
#
# @app.route("start_game", methods=["GET"])
# def start_game():
#    pass
#

###
#  Question Database Routes
###

# TODO
# @app.route("question_menu", methods=["GET"])
# def question_menu():
#    return render_template(QUESTIONS_MENU)


# CREATE a question
@app.route("/create_question", methods=["GET", "POST"])
def create_question():
    # CREATE prompt page
    if request.method == "GET":
        return render_template(CREATE_QUESTION)

    # CREATE data from page
    question = request.form.get("question", None)
    answer = request.form.get("answer", None)
    category = request.form.get("category", None)
    deck_tags = request.form.get("deck_tags", [])

    # 1. Find or create category
    table_category = Category.query.filter_by(name=category).first()
    # db.session.query(Category).filter(Category.name == category).first()
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
    if deck_tags:
        all_tags = deck_tags.split()
        for tag_name in all_tags:
            tag = DeckTag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = DeckTag(name=tag_name)
                db.session.add(tag)
                db.session.flush()
            table_question.deck_tags.append(tag)

    db.session.commit()

    response_msg = "question commited!"
    return render_template(CREATE_QUESTION, response_message=response_msg)


# READ
@app.route("/questions", methods=["GET"])
@app.route("/question/<int:question_id>", methods=["GET"])
def list_questions(question_id=None):
    # READ 1 question
    if question_id:
        question = Question.query.get_or_404(question_id)
        data = [
            {
                "id": question.id,
                "question": question.question_text,
                "answer": question.answer_text,
                "category": question.category.name,
                "deck_tags": [tag.name for tag in question.deck_tags],
            }
        ]
    # READ all questions
    else:
        questions = Question.query.all()
        data = [
            {
                "id": question.id,
                "question": question.question_text,
                "answer": question.answer_text,
                "category": question.category.name,
                "deck_tags": [tag.name for tag in question.deck_tags],
            }
            for question in questions
        ]
    return render_template(READ_QUESTIONS, questions=data)


def list_question(question_id):
    return render_template(READ_QUESTIONS, questions=data)


# UPDATE a question
@app.route("/update_question", methods=["GET"])
@app.route("/commit_update", methods=["POST"])
def update_question():
    response_msg = ""
    # UPDATE question
    if request.method == "POST":
        question_id = request.form.get("question_id", None)
        question_obj = Question.query.get_or_404(question_id)

        question = request.form.get("question", None)
        answer = request.form.get("answer", None)
        category = request.form.get("category", None)
        deck_tags = request.form.get("deck_tags", None)

        if question:
            question_obj.question_text = question
        if answer:
            question_obj.answer_text = answer
        if category:
            table_category = Category.query.filter_by(name=category).first()
            if not table_category:
                category = Category(name=category)
                db.session.add(category)
            question_obj.category.name = category
        if deck_tags:
            question_obj.deck_tags.clear()
            for tag_name in deck_tags:
                tag = DeckTag.query.filter(name=tag_name).first()
                if not tag:
                    tag = DeckTag(name=tag_name)
                question_obj.deck_tags.append(tag)
        db.session.commit()

        response_msg = "question updated!"
    # UPDATE prompt
    else:
        pass
    return render_template(UPDATE_QUESTION, response_message=response_msg)


@app.route("/delete_question", methods=["GET"])
@app.route("/commit_delete", methods=["POST"])
def delete_question():
    response_msg = ""
    # DELETE question
    if request.method == "POST":
        question_id = request.form.get("question_id", None)
        question = Question.query.get_or_404(question_id)
        for deck_tag in question.deck_tags:
            question.deck_tags.remove(deck_tag)
        db.session.delete(question)
        db.session.commit()

        response_msg = "question deleted!"
    # DELETE prompt
    else:
        pass
    return render_template(DELETE_QUESTION, response_message=response_msg)


if __name__ == "__main__":
    app.run(debug=True)
