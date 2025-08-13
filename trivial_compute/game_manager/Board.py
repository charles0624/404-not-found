import json
import pydantic
import random
import requests

from typing import Optional


# my guess as to what's in the database
class Board_Args(pydantic.BaseModel):
    # do not allow creation of unspecified variables in the class, and do not perform
    # type-conversion
    model_config = pydantic.ConfigDict(extra="forbid", strict=True)

    # generic board name
    name: Optional[str] = None
    # could this be a save state type of deal?  dream-category
    # name + '_' + ordinal position: "newgame_25"
    identifier: str

    db_url: str


class Board:
    def __init__(self):
        self.name = "boardnamevariable"

        # the trivial pursuit board looks like a hub-and-spoke type of object.
        # the hub is 6 spaces away from the rim: this is the spoke.
        # there are 6 spokes, and they are 7 spaces away from each other.
        # the rim is 42 spaces.
        # every spoke is connect to the hub and the rim.
        # the hub and spokes are 31 spaces.
        # every rim-side spoke is connected to the rim-side spoke in front of and behind it via the rim.
        # here, the letter is the spot where the rim-side spoke.
        # the distance from A-F to F-A is 7
        # the distance from A-F  to X is 6
        # all players start at the hub.
        self.board = {
            "A": ["F", "B", "X"],  # -7, 7, 6
            "B": ["A", "C", "X"],
            "C": ["B", "D", "X"],
            "D": ["C", "E", "X"],
            "E": ["D", "F", "X"],
            "F": ["E", "A", "X"],
            "X": ["A", "B", "C", "D", "E", "F", "X"],  # 6,6,6,6,6,6,0
        }

        # colors = "red" "orange" "yellow" "green" "blue" "violet"
        # A = red B: green, SILVER, yellow, violet, SILVER, orange
        #         F: green, SILVER,
        #         X: green
        # B = green
        # C = blue
        # D = orange
        # E = yellow
        # F = violet

        print(self.board)

        self.used_question_ids = []

    def __repr__(self):
        return f"{self.name}"
