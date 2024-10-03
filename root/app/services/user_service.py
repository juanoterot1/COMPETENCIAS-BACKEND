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

    def create_user(self, username, password, full_name, mail, dni, created_at=None, performed_by=None):
        """
        Creates a new user.
        """
        try:
            logger.info(f"Creating a new user with username: {username} and DNI: {dni}")
            new_user = self.user_repository.create_user(
                username=username,
                password=password,
                full_name=full_name,
                mail=mail,
                dni=dni,  # Incluyendo dni
                created_at=created_at
            )

            self.usage_log_service.create_usage_log(
                action=f"Created user with username {username} and DNI {dni}",
                performed_by=performed_by
            )

            return new_user
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise InternalServerError("An internal error occurred while creating the user.")

    def get_user_by_id(self, user_id, performed_by=None):
        """
        Retrieves a user by its ID.
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

    def get_users_paginated(self, page, per_page, username=None, full_name=None, mail=None, dni=None):
        """
        Retrieves a paginated list of users with optional filters.
        
        Parameters:
            page (int): The page number to retrieve.
            per_page (int): The number of users per page.
            username (str): Optional filter by username.
            full_name (str): Optional filter by full name.
            mail (str): Optional filter by email.
            dni (str): Optional filter by DNI.
            
        Returns:
            list of users and total count.
        """
        try:
            logger.info(f"Fetching users with filters - page: {page}, per_page: {per_page}, username: {username}, full_name: {full_name}, mail: {mail}, dni: {dni}")
            users_query = self.user_repository.get_users_paginated(page, per_page, username, full_name, mail, dni)
            
            users = [user.as_dict() for user in users_query.items]
            total = users_query.total
            
            return users, total
        except Exception as e:
            logger.error(f"Error fetching paginated users: {e}")
            raise InternalServerError("An internal error occurred while fetching paginated users.")

    def update_user(self, user_id, username=None, password=None, full_name=None, mail=None, dni=None, performed_by=None):
        """
        Updates an existing user.
        """
        try:
            logger.info(f"Updating user with ID: {user_id}")
            updated_user = self.user_repository.update_user(
                user_id, username, password, full_name, mail, dni  # Incluyendo dni
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
