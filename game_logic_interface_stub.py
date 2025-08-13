from flask import Flask, request, jsonify

from game_session import GameSession
from game_session_manager import GameSessionManager
from dice_service import DiceService
from player_tracker import PlayerTracker
from turn_manager import TurnManager
from rule_engine import RuleEngine
from data_access_stub import QuestionDataAccessStub

app = Flask(__name__)

# full game states
game_session = None
turn_manager = None
rule_engine = None
player_tracker = None
manager = None

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


@app.route("/", methods=["GET"])
def index():
    return "Game Logic API is live!"

if __name__ == '__main__':
    app.run(debug=True)
