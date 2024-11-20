from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.permissions import Permission
from app.models.roles import Role


class PermissionRepository:

    @staticmethod
    def create_permission(permission_name, description=None):
        """
        Crea un nuevo permiso en la base de datos, verificando si ya existe.
        
        Parameters:
            permission_name (str): El nombre del permiso.
            description (str, optional): Descripción del permiso.
        
        Returns:
            Permission: El objeto del permiso recién creado.
        """
        try:
            # Verificar si el permiso ya existe
            existing_permission = Permission.query.filter_by(name=permission_name).first()
            if existing_permission:
                raise ValueError(f"Permission with name '{permission_name}' already exists.")
            
            # Crear el nuevo permiso
            new_permission = Permission(name=permission_name, description=description)
            db.session.add(new_permission)
            db.session.commit()
            return new_permission
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
        except ValueError as ve:
            raise ve

    @staticmethod
    def get_permission_by_id(permission_id):
        """
        Recupera un permiso por su ID.
        
        Parameters:
            permission_id (int): El ID del permiso a recuperar.
        
        Returns:
            Permission or None: El objeto del permiso si se encuentra, de lo contrario None.
        """
        try:
            return Permission.query.get(permission_id)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def get_permissions_paginated(page, per_page, name=None):
        """
        Recupera una lista paginada de permisos con filtro opcional por nombre.

        Parameters:
            page (int): El número de página a recuperar.
            per_page (int): La cantidad de permisos por página.
            name (str, optional): Filtra los permisos por nombre.

        Returns:
            Pagination: Un objeto de paginación con los permisos y la información de paginación.
        """
        try:
            query = Permission.query
            if name:
                query = query.filter(Permission.name.ilike(f"%{name}%"))
            return query.paginate(page=page, per_page=per_page, error_out=False)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def update_permission(permission_id, permission_name=None, description=None):
        """
        Actualiza un permiso existente por su ID.
        
        Parameters:
            permission_id (int): El ID del permiso a actualizar.
            permission_name (str, optional): Nuevo nombre del permiso.
            description (str, optional): Nueva descripción del permiso.
        
        Returns:
            Permission or None: El permiso actualizado si se encuentra, de lo contrario None.
        """
        try:
            permission = Permission.query.get(permission_id)
            if permission is None:
                return None
            
            # Verificar si el nuevo nombre ya existe (en otro permiso)
            if permission_name and Permission.query.filter(Permission.name == permission_name, Permission.id != permission_id).first():
                raise ValueError(f"Permission with name '{permission_name}' already exists.")
            
            if permission_name:
                permission.name = permission_name
            if description:
                permission.description = description
            db.session.commit()
            return permission
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
        except ValueError as ve:
            raise ve

    @staticmethod
    def delete_permission(permission_id):
        """
        Elimina un permiso por su ID.
        
        Parameters:
            permission_id (int): El ID del permiso a eliminar.
        
        Returns:
            Permission or None: El permiso eliminado si se encuentra, de lo contrario None.
        """
        try:
            permission = Permission.query.get(permission_id)
            if permission is None:
                return None
            db.session.delete(permission)
            db.session.commit()
            return permission
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e