
class PlayerTracker:
    def __init__(self, users):
        print("[Stub] PlayerTracker initialized")
        self.players = {user: {"position": 0, "score": 0, "chips": []} for user in users}

    def update_position(self, player, steps):
        self.players[player]["position"] += steps
        print(f"[Stub] {player} moved to position {self.players[player]['position']}")

    def add_chip(self, player, chip):
        self.players[player]["chips"].append(chip)
        print(f"[Stub] {player} received chip: {chip}")
