from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.roles import Role
from app.models.permissions import Permission  # Importar el modelo de permisos

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
    def assign_permissions_to_role(role_id, permission_ids):
        """
        Asigna una lista de permisos a un rol.
        
        Parameters:
            role_id (int): ID del rol al que se le asignarán permisos.
            permission_ids (list[int]): Lista de IDs de permisos a asignar.

        Returns:
            Role: El rol con los permisos actualizados.
        """
        try:
            role = Role.query.get(role_id)
            if not role:
                return None

            # Limpiar permisos existentes
            role.permissions = []
            # Agregar nuevos permisos
            for permission_id in permission_ids:
                permission = Permission.query.get(permission_id)
                if permission:
                    role.permissions.append(permission)

            db.session.commit()
            return role
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

            # Usar paginate de SQLAlchemy
            paginated_roles = query.paginate(page=page, per_page=per_page, error_out=False)

            # Devolver los items y el total de la paginación
            return paginated_roles.items, paginated_roles.total
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
