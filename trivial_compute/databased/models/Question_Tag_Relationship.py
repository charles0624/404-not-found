from sqlalchemy import Column, Integer, ForeignKey
from .base import Base

# Table to hold question to deck relationships (many-to-many)
#    "question_decktag",
#    db.Column("question_id", db.Integer, db.ForeignKey("questions.id")),
#    db.Column("decktag_id", db.Integer, db.ForeignKey("deck_tags.id")),

class Question_Decktag(Base):
    __tablename__ = "question_decktag"
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    decktag_id = Column(Integer, ForeignKey("deck_tags.id"))

    def __repr__(self):
        return f"Question: {self.question_id} - {self.decktag_id}"
