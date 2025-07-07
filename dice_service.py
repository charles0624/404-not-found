
import random

class DiceService:
    @staticmethod
    def roll():
        return random.randint(1, 6)
