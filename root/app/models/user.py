from datetime import datetime
from app import db
from models.roles import Role  # Importar el modelo Role

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    mail = db.Column(db.String, nullable=False, unique=True)
    dni = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Clave foránea que referencia a la tabla roles
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    
    # Relación con el modelo Role
    role = db.relationship('Role', backref='users', lazy=True)

    def __init__(self, username, password, full_name, mail, dni, role_id, created_at=None):
        self.username = username
        self.password = password
        self.full_name = full_name
        self.mail = mail
        self.dni = dni
        self.role_id = role_id  # Asignar el rol
        self.created_at = created_at or datetime.utcnow()

    def as_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "full_name": self.full_name,
            "mail": self.mail,
            "dni": self.dni,
            "role_id": self.role_id,  # Incluir el rol en la salida
            "created_at": self.created_at
        }

    def __repr__(self):
        return f"<User {self.username}>"
