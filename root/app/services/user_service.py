import logging
from flask_injector import inject
from werkzeug.exceptions import InternalServerError, NotFound, BadRequest
from app.repositories.user_repository import UserRepository
from app.services.usage_log_service import UsageLogService

logger = logging.getLogger(__name__)

class UserService:

    @inject
    def __init__(self, user_repository: UserRepository, usage_log_service: UsageLogService):
        self.user_repository = user_repository
        self.usage_log_service = usage_log_service

    def create_user(self, username, password, full_name, mail, dni, role_id, created_at=None, performed_by=None):
        """
        Creates a new user.
        
        Parameters:
            username (str): The username of the user.
            password (str): The password of the user.
            full_name (str): The full name of the user.
            mail (str): The email of the user.
            dni (str): The DNI of the user.
            role_id (int): The ID of the role to assign to the user.
            created_at (datetime, optional): The creation date.
            performed_by (int, optional): The ID of the user performing the action.
        
        Returns:
            User: The newly created user object.
        """
        try:
            logger.info(f"Creating a new user with username: {username}, DNI: {dni}, and role ID: {role_id}")
            new_user = self.user_repository.create_user(
                username=username,
                password=password,
                full_name=full_name,
                mail=mail,
                dni=dni,
                role_id=role_id,  # Asignando el rol al crear el usuario
                created_at=created_at
            )

            self.usage_log_service.create_usage_log(
                action=f"Created user with username {username}, DNI {dni}, and role ID {role_id}",
                performed_by=performed_by
            )

            return new_user
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise InternalServerError("An internal error occurred while creating the user.")

    def get_user_by_id(self, user_id, performed_by=None):
        """
        Retrieves a user by its ID.
        
        Parameters:
            user_id (int): The ID of the user to retrieve.
            performed_by (int, optional): The ID of the user performing the action.
        
        Returns:
            User or None: The user object if found, otherwise None.
        """
        try:
            logger.info(f"Fetching user with ID: {user_id}")
            user = self.user_repository.get_user_by_id(user_id)

            if not user:
                logger.info(f"User with ID {user_id} not found.")
                raise NotFound("User not found.")

            self.usage_log_service.create_usage_log(
                action=f"Fetched user with ID {user_id}",
                performed_by=performed_by
            )

            return user
        except NotFound as e:
            logger.warning(f"Not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error fetching user by ID {user_id}: {e}")
            raise InternalServerError("An internal error occurred while fetching the user.")

    def get_users_paginated(self, page, per_page, username=None, full_name=None, mail=None, dni=None, role_id=None):
        """
        Retrieves a paginated list of users with optional filters.
        
        Parameters:
            page (int): The page number to retrieve.
            per_page (int): The number of users per page.
            username (str, optional): Filter by username.
            full_name (str, optional): Filter by full name.
            mail (str, optional): Filter by email.
            dni (str, optional): Filter by DNI.
            role_id (int, optional): Filter by role ID.
            
        Returns:
            list of users and total count.
        """
        try:
            logger.info(f"Fetching users with filters - page: {page}, per_page: {per_page}, role ID: {role_id}")
            users_query = self.user_repository.get_users_paginated(page, per_page, username, full_name, mail, dni, role_id)
            
            users = [user.as_dict() for user in users_query.items]
            total = users_query.total
            
            return users, total
        except Exception as e:
            logger.error(f"Error fetching paginated users: {e}")
            raise InternalServerError("An internal error occurred while fetching paginated users.")

    def update_user(self, user_id, username=None, password=None, full_name=None, mail=None, dni=None, role_id=None, performed_by=None):
        """
        Updates an existing user.
        
        Parameters:
            user_id (int): The ID of the user to update.
            username (str, optional): The new username.
            password (str, optional): The new password.
            full_name (str, optional): The new full name.
            mail (str, optional): The new email.
            dni (str, optional): The new DNI.
            role_id (int, optional): The new role ID.
            performed_by (int, optional): The ID of the user performing the action.
        
        Returns:
            User or None: The updated user object if found, otherwise None.
        """
        try:
            logger.info(f"Updating user with ID: {user_id}")
            updated_user = self.user_repository.update_user(
                user_id, username, password, full_name, mail, dni, role_id  # Actualizando role_id
            )

            if not updated_user:
                logger.info(f"User with ID {user_id} not found.")
                raise NotFound("User not found.")

            self.usage_log_service.create_usage_log(
                action=f"Updated user with ID {user_id}",
                performed_by=performed_by
            )

            return updated_user
        except NotFound as e:
            logger.warning(f"Not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error updating user with ID {user_id}: {e}")
            raise InternalServerError("An internal error occurred while updating the user.")

    def delete_user(self, user_id, performed_by=None):
        """
        Deletes an existing user.
        
        Parameters:
            user_id (int): The ID of the user to delete.
            performed_by (int, optional): The ID of the user performing the action.
        
        Returns:
            User or None: The deleted user object if found, otherwise None.
        """
        try:
            logger.info(f"Deleting user with ID: {user_id}")
            result = self.user_repository.delete_user(user_id)

            if not result:
                logger.warning(f"User with ID {user_id} not found.")
                raise NotFound(f"User with ID {user_id} not found.")

            self.usage_log_service.create_usage_log(
                action=f"Deleted user with ID {user_id}",
                performed_by=performed_by
            )

            return result
        except Exception as e:
            logger.error(f"Error deleting user with ID {user_id}: {e}")
            raise InternalServerError("An internal error occurred while deleting the user.")
