from flask import Blueprint, request, jsonify
from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
from werkzeug.security import check_password_hash
from app.services.user_service import UserService
from app.utils.api_response import ApiResponse
from app.utils.jwt_utils import create_jwt_token
from app.utils.jwt_decorator import jwt_required
from app.utils.permission_decorator import requires_permission
import logging

logger = logging.getLogger(__name__)

user_bp = Blueprint('users', __name__)

@user_bp.route('/login', methods=['POST'])
def login(user_service: UserService):
    """
    Endpoint to log in and generate a JWT token.
    
    Expected JSON body:
        {
            "username": "example",
            "password": "password123"
        }
    """
    try:
        data = request.get_json()
        if not data:
            raise BadRequest("Request body must be provided")

        username = data.get('username')
        password = data.get('password')

        user = user_service.get_user_by_username(username)

        if user and check_password_hash(user.password, password):
            token = create_jwt_token({"user_id": user.id, "username": user.username, "role": user.role_id})
            return jsonify(access_token=token), 200
        else:
            return jsonify({"msg": "Invalid credentials"}), 401

    except BadRequest as e:
        logger.error(f"Bad request: {e}")
        return ApiResponse.bad_request(message=str(e))
    except Exception as e:
        logger.error(f"Error during login: {e}")
        return ApiResponse.internal_server_error()

@user_bp.route('/users', methods=['POST'])
#@jwt_required
#@requires_permission('create_users') 
@inject
def create_user(user_service: UserService):
    """
    Endpoint to create a new user.
    
    Expected JSON body:
        {
            "username": "example",
            "password": "password123",
            "full_name": "John Doe",
            "mail": "example@mail.com",
            "dni": "12345678",
            "role_id": 1,
            "created_at": "2024-09-28T12:34:56",
            "performed_by": "admin"
        }
    """
    try:
        data = request.get_json()
        if not data:
            raise BadRequest("Request body must be provided")

        new_user = user_service.create_user(
            username=data.get('username'),
            password=data.get('password'),
            full_name=data.get('full_name'),
            mail=data.get('mail'),
            dni=data.get('dni'),
            role_id=data.get('role_id'),  # Asignando role_id
            created_at=data.get('created_at'),
            performed_by=data.get('performed_by')
        )

        return ApiResponse.created(result=new_user.as_dict())

    except BadRequest as e:
        logger.error(f"Bad request: {e}")
        return ApiResponse.bad_request(message=str(e))
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        return ApiResponse.internal_server_error()

@user_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required
@requires_permission('view_user')
@inject
def get_user_by_id(user_id, user_service: UserService):
    """
    Endpoint to get a user by ID.
    
    URL parameter:
        user_id (int): The ID of the user to fetch.
    """
    try:
        logger.info(f"Fetching user with ID: {user_id}")
        user = user_service.get_user_by_id(user_id)

        if not user:
            raise NotFound("User not found")

        return ApiResponse.ok(result=user.as_dict())

    except NotFound as e:
        logger.warning(f"User not found: {e}")
        return ApiResponse.not_found(resource="User", resource_id=user_id)
    except Exception as e:
        logger.error(f"Error fetching user by ID {user_id}: {e}")
        return ApiResponse.internal_server_error()

@user_bp.route('/users', methods=['GET'])
@jwt_required
@requires_permission('view_users') 
@inject
def get_users(user_service: UserService):
    """
    Retrieves a paginated list of users with optional filters.
    
    Query Params:
        page (int): The page number to retrieve.
        per_page (int): The number of users per page.
        username (str): Filter by username.
        full_name (str): Filter by full name.
        mail (str): Filter by email.
        dni (str): Filter by dni.
        role_id (int): Filter by role ID.

    Returns:
        Response: JSON response with paginated users or error message.
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        username = request.args.get('username', type=str)
        full_name = request.args.get('full_name', type=str)
        mail = request.args.get('mail', type=str)
        dni = request.args.get('dni', type=str)
        role_id = request.args.get('role_id', type=int)

        logger.info(f"Fetching users with filters - page: {page}, per_page: {per_page}, username: {username}, full_name: {full_name}, mail: {mail}, dni: {dni}, role_id: {role_id}")
        
        users, total = user_service.get_users_paginated(page, per_page, username, full_name, mail, dni, role_id)

        # Calcular si hay páginas siguientes y anteriores
        has_next = (page * per_page) < total
        has_prev = page > 1

        return ApiResponse.ok(
            result=users,
            total=total,
            page=page,
            per_page=per_page,
            has_next=has_next,
            has_prev=has_prev
        )

    except BadRequest as e:
        logger.warning(f"Bad request: {e}")
        return ApiResponse.bad_request(message=str(e))
    except Exception as e:
        logger.error(f"An error occurred while fetching paginated users: {e}")
        return ApiResponse.internal_server_error()

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required
@requires_permission('update_users') 
@inject
def update_user(user_id, user_service: UserService):
    """
    Endpoint to update an existing user.
    
    URL parameter:
        user_id (int): The ID of the user to update.
    Expected JSON body:
        {
            "username": "newusername",
            "password": "newpassword",
            "full_name": "New Full Name",
            "mail": "newemail@mail.com",
            "dni": "87654321",
            "role_id": 2,
            "performed_by": "admin"
        }
    """
    try:
        data = request.get_json()
        if not data:
            raise BadRequest("Request body must be provided")

        updated_user = user_service.update_user(
            user_id=user_id,
            username=data.get('username'),
            password=data.get('password'),
            full_name=data.get('full_name'),
            mail=data.get('mail'),
            dni=data.get('dni'),
            role_id=data.get('role_id'),  # Incluyendo role_id
            performed_by=data.get('performed_by')
        )

        if not updated_user:
            raise NotFound("User not found")

        return ApiResponse.ok(result=updated_user.as_dict(), message="User updated successfully.")

    except BadRequest as e:
        logger.error(f"Bad request: {e}")
        return ApiResponse.bad_request(message=str(e))
    except NotFound as e:
        logger.warning(f"User not found: {e}")
        return ApiResponse.not_found(resource="User", resource_id=user_id)
    except Exception as e:
        logger.error(f"Error updating user: {e}")
        return ApiResponse.internal_server_error()

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required
@requires_permission('delete_users') 
@inject
def delete_user(user_id, user_service: UserService):
    """
    Endpoint to delete a user by ID.
    
    URL parameter:
        user_id (int): The ID of the user to delete.
    """
    try:
        logger.info(f"Deleting user with ID: {user_id}")
        deleted_user = user_service.delete_user(user_id)

        if not deleted_user:
            raise NotFound("User not found")

        return ApiResponse.ok(message="User deleted successfully.")

    except NotFound as e:
        logger.warning(f"User not found: {e}")
        return ApiResponse.not_found(resource="User", resource_id=user_id)
    except Exception as e:
        logger.error(f"Error deleting user with ID {user_id}: {e}")
        return ApiResponse.internal_server_error()