from datetime import datetime
from app import db


class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, role_name):
        self.role_name = role_name
        self.created_at = datetime.utcnow()

    def as_dict(self):
        return {
            "id": self.id,
            "role_name": self.role_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def __repr__(self):
        return f"<Role {self.role_name}>"
