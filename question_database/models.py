from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Table to hold question to deck relationships (many-to-many)
question_decktag = db.Table('question_decktag',
                            db.Column('question_id', db.Integer, db.ForeignKey('question.id')),
                            db.Column('deck_id', db.Integer, db.ForeignKey('deck.id'))
                            )

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    questions = db.relationship('Question', backref='category', lazy='dynamic')

class DeckTag(db.Model):
    __tablename__ = 'deck_tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    deck_tags = db.relationship(
        'DeckTag',
        secondary=question_decktag,
        backref=db.backref('question', lazy='dynamic')
    )