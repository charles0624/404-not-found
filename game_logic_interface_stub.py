
from flask import Flask, request, jsonify
from game_session import GameSession
from dice_service import DiceService

app = Flask(__name__)

# game object
game_session = None

@app.route('/api/settings', methods=['POST'])
def setup_game():
    global game_session
    data = request.get_json()
    users = data.get("users", [])
    topics = data.get("topics", [])
    game_session = GameSession(users, topics)
    print(f"[DEBUG] Game session created with users: {users}, topics: {topics}")
    return jsonify({"status": "game session initialized", "players": users})

@app.route('/api/roll-dice', methods=['POST'])
def roll_dice():
    data = request.get_json()
    player = data.get("player", "Unknown")
    roll = DiceService.roll()
    print(f"[DEBUG] Player '{player}' rolled a {roll}")
    valid_moves = [f"Space {i}" for i in range(1, roll + 1)]  # location
    return jsonify({"roll": roll, "validMoves": valid_moves})

if __name__ == '__main__':
    app.run(debug=True)
