from datetime import datetime
from app import db
from models.evaluation import Evaluation  

class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    value = db.Column(db.Float, nullable=False)
    id_evaluation = db.Column(db.Integer, db.ForeignKey('evaluations.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relación con Evaluations
    evaluation = db.relationship('Evaluation', backref='questions', lazy=True)

    def __init__(self, name, value, id_evaluation):
        self.name = name
        self.value = value
        self.id_evaluation = id_evaluation
        self.created_at = datetime.utcnow()

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "value": self.value,
            "id_evaluation": self.id_evaluation,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def __repr__(self):
        return f"<Question {self.name}>"
