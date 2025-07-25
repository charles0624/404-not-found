
class TurnManager:
    def __init__(self, users):
        self.users = users
        self.current_index = 0
        print("[Stub] TurnManager initialized with users:", users)

    def get_next_player(self):
        player = self.users[self.current_index]
        print(f"[Stub] It's now {player}'s turn.")
        self.current_index = (self.current_index + 1) % len(self.users)
        return player
