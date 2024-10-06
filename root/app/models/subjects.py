from datetime import datetime
from app import db
from models.faculties import Faculty

class Subject(db.Model):
    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    code = db.Column(db.String, nullable=True)
    id_faculty = db.Column(db.Integer, db.ForeignKey('faculties.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # Relación con Facultad
    faculty = db.relationship('Faculty', backref='subjects', lazy=True)

    def __init__(self, name, code, id_faculty):
        self.name = name
        self.code = code
        self.id_faculty = id_faculty
        self.created_at = datetime.utcnow()

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "id_faculty": self.id_faculty,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def __repr__(self):
        return f"<Subject {self.name}>"
