import pydantic
import uuid

import Card

# my guess as to what's in the database
class Deck_Args(pydantic.BaseModel):
    # do not allow creation of unspecified variables in the class
    model_config = pydantic.ConfigDict(extra='forbid', strict=True)

    # "science_class", "sat_prep", "freshman_english", etc...
    name: str
    # "questions about australia's politcal history"
    description: str
    identifier: uuid.UUID

class Deck():
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.database_identifier = uuid.uuid4()

    def __repr__(self):
        return f"{self.name} : {self.description}"

    def get_name(self) -> str:
        return self.name

    def set_name(self, new_name) -> None:
        self.name = new_name
        return

    def list_cards(self) -> None:
        # cycle through database and print all relevant cards
        pass

    def add_card(self, ):
        # add a card to the database
        pass
