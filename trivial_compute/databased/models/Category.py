from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    questions = relationship("Question", backref="category", lazy="dynamic")

    def __repr__(self):
        return f"<Category(name='{self.name}')>"
