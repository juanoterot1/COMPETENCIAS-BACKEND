from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.roles import Role

class RoleRepository:

    @staticmethod
    def create_role(role_name):
        """
        Crea un nuevo rol y lo guarda en la base de datos.
        """
        try:
            new_role = Role(role_name=role_name)
            db.session.add(new_role)
            db.session.commit()
            return new_role
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_role_by_id(role_id):
        """
        Busca un rol por su ID.
        """
        try:
            return Role.query.get(role_id)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def get_roles_paginated(page, per_page, role_name=None):
        """
        Devuelve una lista paginada de roles, con filtro opcional por nombre.
        """
        try:
            query = Role.query
            
            # Filtrar por nombre de rol si está presente
            if role_name:
                query = query.filter(Role.role_name.ilike(f"%{role_name}%"))
            
            return query.paginate(page=page, per_page=per_page, error_out=False)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def update_role(role_id, role_name=None):
        """
        Actualiza un rol existente por su ID.
        """
        try:
            role = Role.query.get(role_id)
            if role is None:
                return None

            # Actualizar los campos proporcionados
            if role_name:
                role.role_name = role_name

            db.session.commit()
            return role
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_role(role_id):
        """
        Elimina un rol por su ID.
        """
        try:
            role = Role.query.get(role_id)
            if role is None:
                return None

            db.session.delete(role)
            db.session.commit()
            return role
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
