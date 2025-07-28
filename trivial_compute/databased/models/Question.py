from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from .base import Base


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    question_text = Column(Text, nullable=False)
    answer_text = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    deck_tags = relationship(
        "DeckTag",
        secondary="question_decktag",
        backref="question",
        lazy="dynamic",
    )

    def __repr__(self):
        return f"Question: {self.question_text} - {self.answer_text}"
