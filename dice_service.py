
import random

class DiceService:
    @staticmethod
    def roll():
        value = random.randint(1, 6)
        print(f"[Stub] Dice rolled: {value}")
        return value
