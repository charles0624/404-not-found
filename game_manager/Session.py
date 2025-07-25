import pydantic

from Board import Board
from Dice import Die
from User import User

# my guess as to what's in the database
class Session_Args(pydantic.BaseModel):
    # do not allow creation of unspecified variables in the class, and do not perform
    # type-conversion
    model_config = pydantic.ConfigDict(extra='forbid', strict=True)

    # generic board name
    board: str
    # could this be a save state type of deal?  dream-category
    # name + '_' + ordinal position: "newgame_25"
    players: list = ""


class Session():
    def __init__(self, board, players):
        self.name = "Demo"
        self.board = board
        self.players = players

    def __repr__(self):
        return f"{self.name} : {self.players}"

    def roll_die(self) -> int:
        return Die.roll()
