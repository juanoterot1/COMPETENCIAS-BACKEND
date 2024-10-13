import logging
from flask_injector import inject
from werkzeug.exceptions import InternalServerError, NotFound
from app.repositories.role_repository import RoleRepository
from app.services.usage_log_service import UsageLogService

logger = logging.getLogger(__name__)

class RoleService:

    @inject
    def __init__(self, role_repository: RoleRepository, usage_log_service: UsageLogService):
        self.role_repository = role_repository
        self.usage_log_service = usage_log_service

    def create_role(self, role_name, id_user=None):
        try:
            logger.info(f"Creating a new role: {role_name}")
            new_role = self.role_repository.create_role(role_name=role_name)

            self.usage_log_service.create_usage_log(
                action=f"Created role {role_name}",
                performed_by=id_user
            )

            return new_role
        except Exception as e:
            logger.error(f"Error creating role: {e}")
            raise InternalServerError("An internal error occurred while creating the role.")

    def get_role_by_id(self, role_id, id_user=None):
        try:
            logger.info(f"Fetching role with ID: {role_id}")
            role = self.role_repository.get_role_by_id(role_id)

            if not role:
                logger.info(f"Role with ID {role_id} not found.")
                raise NotFound("Role not found.")

            self.usage_log_service.create_usage_log(
                action=f"Fetched role with ID {role_id}",
                performed_by=id_user
            )

            return role
        except NotFound as e:
            logger.warning(f"Not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error fetching role by ID {role_id}: {e}")
            raise InternalServerError("An internal error occurred while fetching the role.")

    def get_roles_paginated(self, page, per_page, role_name=None):
        try:
            logger.info(f"Fetching roles with filters - page: {page}, per_page: {per_page}, role_name: {role_name}")
            roles, total = self.role_repository.get_roles_paginated(page, per_page, role_name)

            # Convertir los roles a diccionario si es necesario
            roles_as_dict = [role.as_dict() for role in roles]

            return roles_as_dict, total
        except Exception as e:
            logger.error(f"Error fetching paginated roles: {e}")
            raise InternalServerError("An internal error occurred while fetching paginated roles.")

    def update_role(self, role_id, role_name=None, id_user=None):
        try:
            logger.info(f"Updating role with ID: {role_id}")
            updated_role = self.role_repository.update_role(
                role_id=role_id,
                role_name=role_name
            )

            if not updated_role:
                logger.info(f"Role with ID {role_id} not found.")
                raise NotFound("Role not found.")

            self.usage_log_service.create_usage_log(
                action=f"Updated role with ID {role_id}",
                performed_by=id_user
            )

            return updated_role
        except NotFound as e:
            logger.warning(f"Not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error updating role with ID {role_id}: {e}")
            raise InternalServerError("An internal error occurred while updating the role.")

    def delete_role(self, role_id, id_user=None):
        try:
            logger.info(f"Deleting role with ID: {role_id}")
            result = self.role_repository.delete_role(role_id)

            if not result:
                logger.warning(f"Role with ID {role_id} not found.")
                raise NotFound(f"Role with ID {role_id} not found.")

            self.usage_log_service.create_usage_log(
                action=f"Deleted role with ID {role_id}",
                performed_by=id_user
            )

            return result
        except Exception as e:
            logger.error(f"Error deleting role with ID {role_id}: {e}")
            raise InternalServerError("An internal error occurred while deleting the role.")
