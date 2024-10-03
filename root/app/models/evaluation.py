from datetime import datetime
from app import db

class Evaluation(db.Model):
    __tablename__ = 'evaluations'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, id, name, description=None, created_at=None):
        self.id = id  # Ahora acepta el id como argumento
        self.name = name
        self.description = description
        self.created_at = created_at or datetime.utcnow()

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at
        }

    def __repr__(self):
        return f"<Evaluation {self.name}>"
