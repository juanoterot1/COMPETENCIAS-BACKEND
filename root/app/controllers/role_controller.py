from flask import Blueprint, request
from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
from app.services.role_service import RoleService
from app.utils.api_response import ApiResponse
from app.utils.jwt_decorator import jwt_required
import logging

logger = logging.getLogger(__name__)

role_bp = Blueprint('roles', __name__)

@role_bp.route('/roles', methods=['POST'])
@jwt_required
@inject
def create_role(role_service: RoleService):
    try:
        data = request.get_json()
        if not data or 'role_name' not in data:
            raise BadRequest("role_name must be provided")

        new_role = role_service.create_role(
            role_name=data.get('role_name'),
            id_user=data.get('id_user')
        )

        return ApiResponse.created(result=new_role.as_dict())

    except BadRequest as e:
        logger.error(f"Bad request: {e}")
        return ApiResponse.bad_request(message=str(e))
    except Exception as e:
        logger.error(f"Error creating role: {e}")
        return ApiResponse.internal_server_error()

@role_bp.route('/roles/<int:role_id>', methods=['GET'])
@jwt_required
@inject
def get_role_by_id(role_id, role_service: RoleService):
    try:
        logger.info(f"Fetching role with ID: {role_id}")
        role = role_service.get_role_by_id(role_id)

        if not role:
            raise NotFound("Role not found")

        return ApiResponse.ok(result=role.as_dict())

    except NotFound as e:
        logger.warning(f"Role not found: {e}")
        return ApiResponse.not_found(resource="Role", resource_id=role_id)
    except Exception as e:
        logger.error(f"Error fetching role by ID {role_id}: {e}")
        return ApiResponse.internal_server_error()

@role_bp.route('/roles', methods=['GET'])
@jwt_required
@inject
def get_roles(role_service: RoleService):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        role_name = request.args.get('role_name', type=str)

        logger.info(f"Fetching roles with filters - page: {page}, per_page: {per_page}, role_name: {role_name}")
        
        roles, total = role_service.get_roles_paginated(page, per_page, role_name)

        has_next = (page * per_page) < total
        has_prev = page > 1

        return ApiResponse.ok(
            result=roles,
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
        logger.error(f"An error occurred while fetching paginated roles: {e}")
        return ApiResponse.internal_server_error()

@role_bp.route('/roles/<int:role_id>', methods=['PUT'])
@jwt_required
@inject
def update_role(role_id, role_service: RoleService):
    try:
        data = request.get_json()
        if not data or 'role_name' not in data:
            raise BadRequest("role_name must be provided")

        updated_role = role_service.update_role(
            role_id=role_id,
            role_name=data.get('role_name'),
            id_user=data.get('id_user')
        )

        if not updated_role:
            raise NotFound("Role not found")

        return ApiResponse.ok(result=updated_role.as_dict(), message="Role updated successfully.")

    except BadRequest as e:
        logger.error(f"Bad request: {e}")
        return ApiResponse.bad_request(message=str(e))
    except NotFound as e:
        logger.warning(f"Role not found: {e}")
        return ApiResponse.not_found(resource="Role", resource_id=role_id)
    except Exception as e:
        logger.error(f"Error updating role: {e}")
        return ApiResponse.internal_server_error()

@role_bp.route('/roles/<int:role_id>', methods=['DELETE'])
@jwt_required
@inject
def delete_role(role_id, role_service: RoleService):
    try:
        logger.info(f"Deleting role with ID: {role_id}")
        deleted_role = role_service.delete_role(role_id)

        if not deleted_role:
            raise NotFound("Role not found")

        return ApiResponse.ok(message="Role deleted successfully.")

    except NotFound as e:
        logger.warning(f"Role not found: {e}")
        return ApiResponse.not_found(resource="Role", resource_id=role_id)
    except Exception as e:
        logger.error(f"Error deleting role with ID {role_id}: {e}")
        return ApiResponse.internal_server_error()