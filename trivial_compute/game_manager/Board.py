import json
import pydantic
import random
import requests

from typing import Optional

# needed for web api
DB_URL = "http://127.0.0.1:5000"
HEADERS = {"Content-Type": "application/json"}


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
    def __init__(self, number, db_url, name=None):
        if not name:
            self.name = "boardnamevariable"
        else:
            self.name = name

        self.identifier = f"{self.name}_{number}"

        # any letter to any letter, where neither letter is 'X', has an edge weight of 6
        # any letter to 'X', has an edge weight of 5
        self.board = {
            "A": ["F", "B", "X"],
            "B": ["A", "C", "X"],
            "C": ["B", "D", "X"],
            "D": ["C", "E", "X"],
            "E": ["D", "F", "X"],
            "F": ["E", "A", "X"],
            "X": ["A", "B", "C", "D", "E", "F"],
        }

        self.used_question_ids = []

    def __repr__(self):
        return f"{self.name} : {self.identifier}"

    # TODO: associate board spaces with colors -> trivia categories

    def ask_question(self, boardspace) -> None:
        # TODO: get quantity of cards in deck
        selection = random.randint(1, 10)
        if not len(self.used_question_ids) == 0:
            while True:
                if not selection in self.used_question_ids:
                    break
                selection = random.randint(1, 10)

        data = {"question_id": selection}
        try:
            response = requests.get(
                f"{DB_URL}/questions/{selection}",
                data=json.dumps(data),
                headers=HEADERS,
            )
            response.raise_for_status()
        except requests.exceptions as err:
            print("ERROR: {err}")
            return 0

        self.used_question_ids.append(response.json()["id"])
        print(response.json()["question"])

        input("press the 'enter' to reveal the answer...")

        print(response.json()["answer"])

        correct = input("did the player answer correctly? [y/N] ")
        if correct in ("y", "yes", "Y", "YES"):
            print("woot woot!")
            return True
        else:
            print("womp womp!")
            return False
