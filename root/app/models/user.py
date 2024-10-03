from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    mail = db.Column(db.String, nullable=False, unique=True)
    dni = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, password, full_name, mail, dni, created_at=None):
        self.username = username
        self.password = password
        self.full_name = full_name
        self.mail = mail
        self.dni = dni  # Asignar el nuevo campo
        self.created_at = created_at or datetime.utcnow()

    def as_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "full_name": self.full_name,
            "mail": self.mail,
            "dni": self.dni,  # Incluir el nuevo campo
            "created_at": self.created_at
        }

    def __repr__(self):
        return f"<User {self.username}>"
