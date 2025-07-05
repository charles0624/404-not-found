import pydantic
import uuid

class Card(pydantic.BaseModel):
    # do not allow creation of unspecified variables in the class
    model_config = ConfigDict(extra='forbid', strict=True)

    category: str
    decks: list
    question: str
    answer: str
    identifier: UUID
