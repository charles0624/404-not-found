import copy
import random
import sys

# web server and database stuff
from flask import Flask, redirect, render_template, request, jsonify, url_for
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

from models import db, Category, DeckTag, Question
from game_object import COLORS, get_player

from werkzeug.exceptions import NotFound

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
GAME_READY = "game_ready.html"
GAME_SESSION = "game_session.html"

QUESTIONS_MENU = "questions_menu.html"
CREATE_QUESTION = "create_question.html"
READ_QUESTIONS = "questions.html"
UPDATE_QUESTION = "update_question.html"
DELETE_QUESTION = "delete_question.html"


#########
#########
#  Startup Routes
#########
#########
# home page
@app.route("/", methods=["GET"])
def index():
    return render_template(HOME_PAGE)

# quit
@app.route("/exit", methods=["GET"])
def exit():
    sys.exit()  # can't imagine this is recommended

# enter player data
@app.route("/play_game", methods=["GET"])
def play_game():
    return render_template(USERS_MENU)

# interact with question editor
@app.route("/question_menu", methods=["GET"])
def question_menu():
    return render_template(QUESTIONS_MENU)

#########
#########
#  Question Database Routes
#########
#########
# interact with question editor
#@app.route("/question_menu", methods=["GET"])
#def question_menu():
#    return render_template(CREATE_QUESTION)

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
        all_tags = deck_tags.split(':')
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


# UPDATE a question
@app.route("/update_question", methods=["GET"])
@app.route("/commit_update", methods=["POST"])
def update_question():
    response_msg = ""
    # UPDATE question
    if request.method == "POST":
        question_id = request.form.get("question_id", None)

        try:
            question_obj = Question.query.get_or_404(question_id)
        except NotFound:
            response_msg = "Question ID Not Found! Update not Complete."
            return render_template(UPDATE_QUESTION, response_message=response_msg)

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
                table_category = Category(name=category)
                db.session.add(table_category)
                db.session.flush()
            question_obj.category = table_category
        if deck_tags:
            question_obj.deck_tags = []
            for tag_name in deck_tags.split(':'):
                tag = DeckTag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = DeckTag(name=tag_name)
                    db.session.add(tag)
                    db.session.flush()
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

        try:
            question = Question.query.get_or_404(question_id)
        except NotFound:
            response_msg = "Question ID Not Found! Delete not Complete."
            return render_template(DELETE_QUESTION, response_message=response_msg)

        if question.deck_tags:
            for deck_tag in question.deck_tags:
                question.deck_tags.remove(deck_tag)
        db.session.delete(question)
        db.session.commit()

        response_msg = "question deleted!"
    # DELETE prompt
    else:
        pass
    return render_template(DELETE_QUESTION, response_message=response_msg)


#from game_session import GameSession
#from game_session_manager import GameSessionManager
#from dice_service import DiceService
#from player_tracker import PlayerTracker
#from turn_manager import TurnManager
#from rule_engine import RuleEngine
#from data_access_stub import QuestionDataAccessStub

# full game states
game_session = None
turn_manager = None
rule_engine = None
player_tracker = None
manager = None

#########
#########
#  Game Session Routes
#########
#########
def random_color_index(modulo_number):
    return random.randint(0,100) % modulo_number # ensure it is random AND between length of list, inclusive

# get users
@app.route("/users_menu", methods=["GET", "POST"])
def get_users():
    return render_template(USERS_MENU)

# get users
# called from 'users_menu.html'
@app.route("/validate_users", methods=["POST"])
def validate_users():
    # get player names
    player_list = [
        request.form.get("player1"),
        request.form.get("player2"),
        request.form.get("player3"),
        request.form.get("player4")
    ]

    # check that player names are not empty
    real_player_list = list()
    for elem in player_list:
        if len(elem) > 0:
            real_player_list.append(elem)
    if len(real_player_list) == 0:
        data = {"user_data": "fail"}
        return render_template(USERS_MENU, no_users=data)

    # create player objects and assign each one a color
    player_colors = copy.deepcopy(COLORS)
    list_len = len(player_colors)
    player_objs = list()
    for player in real_player_list:
        player_color = player_colors.pop(random_color_index(list_len))
        player_objs.append(get_player(player, player_color))
        list_len -= 1

    # generate the game board, populated with the players objects
    return render_template(USERS_MENU, players=player_objs)

# called from USERS_MENU after correct player validation
@app.route("/game_session", methods=["GET", "POST"])
def game_session():
    return render_template(GAME_SESSION)


# Game Initialization
@app.route('/api/settings', methods=['POST'])
def setup_game():
    global game_session, manager, turn_manager, rule_engine, player_tracker
    data = request.get_json()
    users = data.get("users", [])       # e.g.: ["Alice", "Bob"]
    topics = data.get("topics", [])     # e.g.: ["Math", "Science"]

    game_session = GameSession(users, topics)
    manager = GameSessionManager(users, topics)
    turn_manager = TurnManager(users)
    rule_engine = RuleEngine()
    player_tracker = PlayerTracker(users)

    db = QuestionDataAccessStub()
    question = db.get_mock_question()
    print(f"[Stub] Game Logic received question: {question}")

    return jsonify({"status": "game session initialized", "players": users})


# roll dice
@app.route('/api/roll-dice', methods=['POST'])
def roll_dice():
    data = request.get_json()
    player = data.get("player", "Unknown")
    roll = DiceService.roll()
    print(f"[Stub] Player '{player}' rolled a {roll}")
    valid_moves = [f"Space {i}" for i in range(1, roll + 1)]
    return jsonify({"roll": roll, "validMoves": valid_moves})


# player move
@app.route('/api/move', methods=['POST'])
def move_player():
    data = request.get_json()
    player = data.get("player")
    space = data.get("target")

    # real space change
    player_tracker.update_position(player, 1)
    print(f"[Stub] {player} moved to {space}")

    return jsonify({
        "status": "moved",
        "player": player,
        "newPosition": space
    })


# answer verify and chips allocation
@app.route('/api/answer', methods=['POST'])
def check_answer():
    data = request.get_json()
    player = data.get("player")
    answer = data.get("answer")

    correct = rule_engine.validate_answer(answer)  # always True in staub

    if correct:
        chip = "math"
        player_tracker.add_chip(player, chip)
        print(f"[Stub] {player} answered correctly and earned chip {chip}")
        return jsonify({"correct": True, "chip_awarded": chip})
    else:
        print(f"[Stub] {player} answered incorrectly")
        return jsonify({"correct": False})

if __name__ == "__main__":
    app.run(debug=True)
