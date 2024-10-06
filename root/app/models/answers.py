from datetime import datetime
from app import db
from models.evaluation import Evaluation
from models.question import Question
from models.user import User

class Answer(db.Model):
    __tablename__ = 'answers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    answer_description = db.Column(db.String, nullable=False)
    id_evaluation = db.Column(db.Integer, db.ForeignKey('evaluations.id'), nullable=False)
    id_question = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    score = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relaciones
    evaluation = db.relationship('Evaluation', backref='answers', lazy=True)
    question = db.relationship('Question', backref='answers', lazy=True)
    user = db.relationship('User', backref='answers', lazy=True)

    def __init__(self, answer_description, id_evaluation, id_question, id_user, score=None):
        self.answer_description = answer_description
        self.id_evaluation = id_evaluation
        self.id_question = id_question
        self.id_user = id_user
        self.score = score
        self.created_at = datetime.utcnow()

    def as_dict(self):
        return {
            "id": self.id,
            "answer_description": self.answer_description,
            "id_evaluation": self.id_evaluation,
            "id_question": self.id_question,
            "id_user": self.id_user,
            "score": self.score,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def __repr__(self):
        return f"<Answer {self.answer_description}>"
