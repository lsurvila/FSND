from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)


class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    category = Column(String)
    difficulty = Column(Integer)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, model_type):
        self.type = model_type
