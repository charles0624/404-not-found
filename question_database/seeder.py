# seeder.py
from dataclasses import dataclass
from typing import Iterable
from app import app 
from models import db, Question, Category, DeckTag

@dataclass
class DefaultQuestion:
    question: str
    answer: str
    category: str
    tags: Iterable[str] = ()

class DefaultDataSeeder:
    def __init__(self, app):
        self.app = app

    def run(self) -> None:
        with self.app.app_context():
            db.create_all()

            if Question.query.count() > 0:
                print("Seed skipped: questions already exist.")
                return

            # categories
            cats = {
                name: Category(name=name)
                for name in ["Geography", "History", "Science", "Sports", "Entertainment"]
            }
            db.session.add_all(cats.values())
            db.session.flush()

            # tags
            tags = {name: DeckTag(name=name) for name in ["General", "Beginner", "Classic"]}
            db.session.add_all(tags.values())
            db.session.flush()

            # defaults questions
            defaults = [
                DefaultQuestion("What is the capital of France?", "Paris", "Geography", ("General", "Classic")),
                DefaultQuestion("Which river runs through Egypt?", "Nile", "Geography", ("General",)),
                DefaultQuestion("Who was the first President of the United States?", "George Washington", "History", ("Beginner",)),
                DefaultQuestion("In what year did World War II end?", "1945", "History", ("General", "Classic")),
                DefaultQuestion("What planet is known as the Red Planet?", "Mars", "Science", ("General",)),
                DefaultQuestion("What gas do plants primarily absorb for photosynthesis?", "Carbon Dioxide", "Science", ("Beginner",)),
                DefaultQuestion("How many players are on a standard soccer team on the field?", "11", "Sports", ("General",)),
                DefaultQuestion("Which country has won the most FIFA World Cups?", "Brazil", "Sports", ("Classic",)),
                DefaultQuestion("Who played Jack Dawson in Titanic?", "Leonardo DiCaprio", "Entertainment", ("General",)),
                DefaultQuestion("Which movie features the quote 'May the Force be with you'?", "Star Wars", "Entertainment", ("Classic",)),
            ]

            for dq in defaults:
                q = Question(
                    question_text=dq.question,
                    answer_text=dq.answer,
                    category_id=cats[dq.category].id,
                )
                for t in dq.tags:
                    q.deck_tags.append(tags[t])
                db.session.add(q)

            db.session.commit()
            print("✅ Seeded default questions.")

if __name__ == "__main__":
    DefaultDataSeeder(app).run()
