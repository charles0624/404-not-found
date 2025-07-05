import pydantic

# my guess as to what's in the database
class Board_Args(pydantic.BaseModel):
    # do not allow creation of unspecified variables in the class, and do not perform
    # type-conversion
    model_config = pydantic.ConfigDict(extra='forbid', strict=True)

    # generic board name
    name: list
    # could this be a save state type of deal?  dream-category
    # name + '_' + ordinal position: "newgame_25"
    identifier: str = ""

class Board():
    def __init__(self):
        # need to create 'random_name_generator()'
        #self.name = random_name_generator()
        self.name = "boardnamevariable"
        # add function to see how many games in the database are currently being played
        # number = str(database_read(db, category))
        self.identifier = f"{self.name}_{number}"

    def __repr__(self):
        return f"{self.name} : {self.identifier}"

    def get_category(self) -> str:
        return self.category

    def set_category(self, new_category) -> None:
        self.category = new_category

    def get_question(self) -> str:
        return self.question

    def set_question(self, new_question) -> None:
        self.question = new_question

    def get_answer(self) -> str:
        return self.answer

    def set_answer(self, new_answer) -> None:
        self.answer = new_answer

    def get_deck_memberships(self) -> list:
        return self.deck_names

    def add_deck_membership(self, new_deck) -> None:
        if new_deck not in self.deck_names:
            self.deck_names.append(new_deck)

    def remove_deck_membership(self, old_deck) -> None:
        if old_deck in self.deck_names:
            self.deck_names.remove(old_deck)
