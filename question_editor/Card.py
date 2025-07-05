import pydantic

# my guess as to what's in the database
class Card_Args(pydantic.BaseModel):
    # do not allow creation of unspecified variables in the class, and do not perform
    # type-conversion
    model_config = pydantic.ConfigDict(extra='forbid', strict=True)

    # "Science", "Mathematics", "Biology", "Literature", etc...
    category: str
    # "How many miles are in an astronimcal unit?"
    question: str
    # "149,597,870,700m"
    answer: str
    # "science_class", "sat_prep", "freshman_english", etc...
    deck_names: list
    # category string + '_' + ordinal position: "anatomy_25"
    identifier: str = ""

class Card():
    def __init__(self, category, question, answer, deck_name):
        self.category = category
        self.question = question
        self.answer = answer
        self.deck_names = [deck_name]
        # add function to see how many questions of this category are in the database already
        # number = str(database_read(db, category))
        self.identifier = f"{category}_{number}"

    def __repr__(self):
        return f"{self.category} : {self.deck_names} : {self.question} : {self.answer}"

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
