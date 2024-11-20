from datetime import datetime
from app import db
from .role_permissions import role_permissions  # Importa la tabla intermedia


class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

     # Relación con permisos
    permissions = db.relationship('Permission', secondary='role_permissions', lazy='subquery',backref=db.backref('roles', lazy=True))

    def __init__(self, role_name):
        self.role_name = role_name
        self.created_at = datetime.utcnow()

    def as_dict(self):
        return {
            "id": self.id,
            "role_name": self.role_name,
            "permissions": [permission.as_dict() for permission in self.permissions],
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def __repr__(self):
        return f"<Role {self.role_name}>"
