
class GameSession:
    def __init__(self, users, topics):
        self.users = users
        self.topics = topics
        self.state = "initialized"
