import logging
from flask_injector import inject
from werkzeug.exceptions import InternalServerError, NotFound, BadRequest
from app.repositories.permission_repository import PermissionRepository

logger = logging.getLogger(__name__)

class PermissionService:

    @inject
    def __init__(self, permission_repository: PermissionRepository):
        self.permission_repository = permission_repository

    def create_permission(self, name, description=None):
        """
        Crea un nuevo permiso, verificando que no exista un duplicado.

        Parameters:
            name (str): El nombre del permiso.
            description (str, optional): Descripción del permiso.

        Returns:
            Permission: El objeto del permiso recién creado.
        """
        try:
            logger.info(f"Creating permission with name: {name}")

            # Validar si el permiso ya existe
            existing_permissions = self.permission_repository.get_permissions_paginated(1, 1, name=name)
            if existing_permissions.items:  # Usar .items para acceder a los resultados
                logger.warning(f"Permission with name '{name}' already exists.")
                raise ValueError(f"Permission with name '{name}' already exists.")

            return self.permission_repository.create_permission(name, description)
        except ValueError as ve:
            logger.error(f"Validation error: {ve}")
            raise BadRequest(str(ve))
        except Exception as e:
            logger.error(f"Error creating permission: {e}")
            raise InternalServerError("An internal error occurred while creating the permission.")


    def get_permission_by_id(self, permission_id):
        """
        Recupera un permiso por su ID.

        Parameters:
            permission_id (int): El ID del permiso a recuperar.

        Returns:
            Permission or None: El objeto del permiso si se encuentra, de lo contrario None.
        """
        try:
            logger.info(f"Fetching permission with ID: {permission_id}")
            permission = self.permission_repository.get_permission_by_id(permission_id)

            if not permission:
                logger.info(f"Permission with ID {permission_id} not found.")
                raise NotFound("Permission not found.")

            return permission
        except NotFound as e:
            logger.warning(f"Not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error fetching permission by ID {permission_id}: {e}")
            raise InternalServerError("An internal error occurred while fetching the permission.")

    def get_permissions_paginated(self, page, per_page, name=None):
        """
        Recupera una lista paginada de permisos.

        Parameters:
            page (int): El número de página a recuperar.
            per_page (int): La cantidad de permisos por página.
            name (str, optional): Filtro opcional por nombre del permiso.

        Returns:
            dict: Un diccionario con la lista de permisos y la información de paginación.
        """
        try:
            logger.info(f"Fetching permissions with filters - page: {page}, per_page: {per_page}, name: {name}")
            permissions_query = self.permission_repository.get_permissions_paginated(page, per_page, name)

            permissions = [perm.as_dict() for perm in permissions_query.items]
            return {
                "permissions": permissions,
                "total": permissions_query.total,
                "page": page,
                "per_page": per_page,
                "has_next": permissions_query.has_next,
                "has_prev": permissions_query.has_prev,
            }
        except Exception as e:
            logger.error(f"Error fetching paginated permissions: {e}")
            raise InternalServerError("An internal error occurred while fetching paginated permissions.")

    def update_permission(self, permission_id, name=None, description=None):
        """
        Actualiza un permiso existente.

        Parameters:
            permission_id (int): El ID del permiso a actualizar.
            name (str, optional): Nuevo nombre del permiso.
            description (str, optional): Nueva descripción del permiso.

        Returns:
            Permission or None: El permiso actualizado si se encuentra, de lo contrario None.
        """
        try:
            logger.info(f"Updating permission with ID: {permission_id}")

            # Verificar duplicados solo si se intenta actualizar el nombre
            if name:
                existing_permissions = self.permission_repository.get_permissions_paginated(1, 1, name=name)
                # Usar .items para acceder a la lista de resultados
                if existing_permissions.items and existing_permissions.items[0].id != permission_id:
                    logger.warning(f"Permission with name '{name}' already exists.")
                    raise ValueError(f"Permission with name '{name}' already exists.")

            updated_permission = self.permission_repository.update_permission(permission_id, name, description)

            if not updated_permission:
                logger.info(f"Permission with ID {permission_id} not found.")
                raise NotFound("Permission not found.")

            return updated_permission
        except ValueError as ve:
            logger.error(f"Validation error: {ve}")
            raise BadRequest(str(ve))
        except NotFound as e:
            logger.warning(f"Not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error updating permission with ID {permission_id}: {e}")
            raise InternalServerError("An internal error occurred while updating the permission.")


    def delete_permission(self, permission_id):
        """
        Elimina un permiso existente.

        Parameters:
            permission_id (int): El ID del permiso a eliminar.

        Returns:
            Permission or None: El permiso eliminado si se encuentra, de lo contrario None.
        """
        try:
            logger.info(f"Deleting permission with ID: {permission_id}")
            result = self.permission_repository.delete_permission(permission_id)

            if not result:
                logger.warning(f"Permission with ID {permission_id} not found.")
                raise NotFound(f"Permission with ID {permission_id} not found.")

            logger.info(f"Permission with ID {permission_id} deleted successfully.")
            return result
        except Exception as e:
            logger.error(f"Error deleting permission with ID {permission_id}: {e}")
            raise InternalServerError("An internal error occurred while deleting the permission.")
