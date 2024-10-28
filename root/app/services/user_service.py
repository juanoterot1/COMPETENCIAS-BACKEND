import logging
from flask_injector import inject
from werkzeug.exceptions import InternalServerError, NotFound, BadRequest
from werkzeug.security import generate_password_hash, check_password_hash
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
        Creates a new user with hashed password.
        """
        try:
            hashed_password = generate_password_hash(password)  # Hash the password before saving
            logger.info(f"Creating a new user with username: {username}, DNI: {dni}, and role ID: {role_id}")
            
            new_user = self.user_repository.create_user(
                username=username,
                password=hashed_password,  # Store hashed password
                full_name=full_name,
                mail=mail,
                dni=dni,
                role_id=role_id,
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

    def get_user_by_username(self, username):
        """
        Retrieves a user by their username.
        """
        try:
            logger.info(f"Fetching user with username: {username}")
            user = self.user_repository.get_user_by_username(username)
            
            if not user:
                logger.warning(f"User with username {username} not found.")
                raise NotFound("User not found.")
            
            return user
        except Exception as e:
            logger.error(f"Error fetching user by username {username}: {e}")
            raise InternalServerError("An internal error occurred while fetching the user.")

    def get_user_by_id(self, user_id, performed_by=None):
        """
        Retrieves a user by their ID.
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
        Updates an existing user with optional new hashed password.
        """
        try:
            logger.info(f"Updating user with ID: {user_id}")

            # Hash the new password if provided
            if password:
                password = generate_password_hash(password)
            
            updated_user = self.user_repository.update_user(
                user_id, username, password, full_name, mail, dni, role_id
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
