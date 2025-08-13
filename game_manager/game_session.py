
class GameSession:
    def __init__(self, users, topics):
        self.users = users
        self.topics = topics
        self.state = "initialized"
        print(f"[Stub] GameSession created with users {users} and topics {topics}")
