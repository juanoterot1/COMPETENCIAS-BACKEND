from datetime import datetime
from app import db
from models.faculties import Faculty
from models.subjects import Subject
from models.user import User

class Evaluation(db.Model):
    __tablename__ = 'evaluations'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    id_subject = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    id_faculty = db.Column(db.Integer, db.ForeignKey('faculties.id'), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relaciones
    subject = db.relationship('Subject', backref='evaluations', lazy=True)
    faculty = db.relationship('Faculty', backref='evaluations', lazy=True)
    user = db.relationship('User', backref='evaluations', lazy=True)  # Suponiendo que el modelo User existe

    def __init__(self, id, name, description=None, id_subject=None, id_faculty=None, id_user=None, status=None):
        self.id = id  # Acepta el id como argumento
        self.name = name
        self.description = description
        self.id_subject = id_subject
        self.id_faculty = id_faculty
        self.id_user = id_user
        self.status = status
        self.created_at = datetime.utcnow()

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "id_subject": self.id_subject,
            "id_faculty": self.id_faculty,
            "id_user": self.id_user,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def __repr__(self):
        return f"<Evaluation {self.name}>"
