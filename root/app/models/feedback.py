from datetime import datetime
from app import db

class Feedback(db.Model):
    __tablename__ = 'feedback'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_evaluation = db.Column(db.Integer, db.ForeignKey('evaluations.id'), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relaciones
    evaluation = db.relationship('Evaluation', backref='feedbacks', lazy=True)
    user = db.relationship('User', backref='feedbacks', lazy=True)

    def __init__(self, id_evaluation, id_user, feedback_text):
        self.id_evaluation = id_evaluation
        self.id_user = id_user
        self.feedback_text = feedback_text
        self.created_at = datetime.utcnow()

    def as_dict(self):
        return {
            "id": self.id,
            "id_evaluation": self.id_evaluation,
            "id_user": self.id_user,
            "feedback_text": self.feedback_text,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def __repr__(self):
        return f"<Feedback by User {self.id_user} on Evaluation {self.id_evaluation}>"
