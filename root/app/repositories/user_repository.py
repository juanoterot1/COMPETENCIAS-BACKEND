from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.user import User

class UserRepository:

    @staticmethod
    def create_user(username, password, full_name, mail, dni, role_id, created_at=None):
        """
        Creates a new user in the database.
        
        Parameters:
            username (str): The username of the user.
            password (str): The password of the user.
            full_name (str): The full name of the user.
            mail (str): The email of the user.
            dni (str): The DNI of the user.
            role_id (int): The ID of the role to associate with the user.
            created_at (datetime, optional): The creation date. If not provided, it will use the current time.
        
        Returns:
            User: The newly created user object.
        """
        try:
            new_user = User(
                username=username,
                password=password,
                full_name=full_name,
                mail=mail,
                dni=dni,
                role_id=role_id,  # Agregar role_id al crear usuario
                created_at=created_at
            )
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_user_by_id(user_id):
        """
        Retrieves a user by its ID.
        
        Parameters:
            user_id (int): The ID of the user to retrieve.
        
        Returns:
            User or None: The user object if found, otherwise None.
        """
        try:
            return User.query.get(user_id)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def get_users_paginated(page, per_page, username=None, full_name=None, mail=None, dni=None, role_id=None):
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
            Pagination: A Pagination object containing the users and pagination info.
        """
        try:
            query = User.query
            
            if username:
                query = query.filter(User.username.ilike(f"%{username}%"))
            if full_name:
                query = query.filter(User.full_name.ilike(f"%{full_name}%"))
            if mail:
                query = query.filter(User.mail.ilike(f"%{mail}%"))
            if dni:
                query = query.filter(User.dni.ilike(f"%{dni}%"))
            if role_id:
                query = query.filter(User.role_id == role_id)  # Filtrar por role_id
            
            return query.paginate(page=page, per_page=per_page, error_out=False)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def update_user(user_id, username=None, password=None, full_name=None, mail=None, dni=None, role_id=None):
        """
        Updates an existing user.
        
        Parameters:
            user_id (int): The ID of the user to update.
            username (str, optional): New username.
            password (str, optional): New password.
            full_name (str, optional): New full name.
            mail (str, optional): New email.
            dni (str, optional): New DNI.
            role_id (int, optional): New role ID.
        
        Returns:
            User or None: The updated user object if found, otherwise None.
        """
        try:
            user = User.query.get(user_id)
            if user is None:
                return None

            if username:
                user.username = username
            if password:
                user.password = password
            if full_name:
                user.full_name = full_name
            if mail:
                user.mail = mail
            if dni:
                user.dni = dni
            if role_id:
                user.role_id = role_id  # Actualizar role_id

            db.session.commit()
            return user
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_user(user_id):
        """
        Deletes a user by its ID.
        
        Parameters:
            user_id (int): The ID of the user to delete.
        
        Returns:
            User or None: The deleted user object if found, otherwise None.
        """
        try:
            user = User.query.get(user_id)
            if user is None:
                return None

            db.session.delete(user)
            db.session.commit()
            return user
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
        
    @staticmethod
    def get_user_by_username(username):
        """
        Retrieves a user by its username.
        
        Parameters:
            username (str): The username of the user to retrieve.
        
        Returns:
            User or None: The user object if found, otherwise None.
        """
        try:
            return User.query.filter_by(username=username).first()
        except SQLAlchemyError as e:
            raise e