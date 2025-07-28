from sqlalchemy import Column, Integer, String
from .base import Base


class DeckTag(Base):
    __tablename__ = "deck_tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"Tag {self.name}"
