from editor_logic_stub import EditorLogicStub
from data_access_stub import QuestionDataAccessStub
from flask import Flask, request, jsonify
from game_session import GameSession
from dice_service import DiceService
from game_session_manager import GameSessionManager
from turn_manager import TurnManager
from rule_engine import RuleEngine
from player_tracker import PlayerTracker

app = Flask(__name__)

game_session = None
turn_manager = None
rule_engine = None
player_tracker = None
manager = None

@app.route('/api/settings', methods=['POST'])
def setup_game():
    global game_session, manager, turn_manager, rule_engine, player_tracker
    data = request.get_json()
    users = data.get("users", [])
    topics = data.get("topics", [])
    game_session = GameSession(users, topics)
    manager = GameSessionManager(users, topics)
    turn_manager = TurnManager(users)
    rule_engine = RuleEngine()
    player_tracker = PlayerTracker(users)

    # subsystem communication
    editor = EditorLogicStub()
    editor.respond_to_game_logic()

    db = QuestionDataAccessStub()
    question = db.get_mock_question()
    print(f"[Stub] Game Logic received question: {question}")

    return jsonify({"status": "game session initialized", "players": users})

@app.route('/api/roll-dice', methods=['POST'])
def roll_dice():
    global turn_manager
    data = request.get_json()
    player = data.get("player", "Unknown")
    roll = DiceService.roll()
    print(f"[Stub] Player '{player}' rolled a {roll}")
    valid_moves = [f"Space {i}" for i in range(1, roll + 1)]
    return jsonify({"roll": roll, "validMoves": valid_moves})

if __name__ == '__main__':
    app.run(debug=True)
