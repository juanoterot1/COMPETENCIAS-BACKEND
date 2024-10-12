from datetime import datetime
from app import db
from models.subjects import Subject

class GradingMatrix(db.Model):
    __tablename__ = 'grading_matrix'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_subject = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    total_evaluations = db.Column(db.Integer, nullable=False)
    total_score = db.Column(db.Float, nullable=False)
    recommendation = db.Column(db.String, nullable=True)
    score = db.Column(db.Float, nullable=False)
    document = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relación con Subject
    subject = db.relationship('Subject', backref='grading_matrices', lazy=True)

    def __init__(self, id_subject, total_evaluations, total_score, score, recommendation=None, document=None):
        self.id_subject = id_subject
        self.total_evaluations = total_evaluations
        self.total_score = total_score
        self.recommendation = recommendation
        self.score = score
        self.document = document
        self.created_at = datetime.utcnow()

    def as_dict(self):
        return {
            "id": self.id,
            "id_subject": self.id_subject,
            "total_evaluations": self.total_evaluations,
            "total_score": self.total_score,
            "recommendation": self.recommendation,
            "score": self.score,
            "document": self.document,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def __repr__(self):
        return f"<GradingMatrix for Subject {self.id_subject}>"
