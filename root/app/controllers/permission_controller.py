from flask import Blueprint, request
from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
from app.services.permission_service import PermissionService
from app.utils.api_response import ApiResponse
import logging

logger = logging.getLogger(__name__)

permission_bp = Blueprint('permissions', __name__)


@permission_bp.route('/permissions', methods=['POST'])
@inject
def create_permission(permission_service: PermissionService):
    """
    Crea un nuevo permiso.
    
    Expected JSON body:
        {
            "name": "create_roles",
            "description": "Permission to create roles"
        }
    """
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            raise BadRequest("Permission name is required.")

        new_permission = permission_service.create_permission(
            name=data['name'],
            description=data.get('description')
        )

        return ApiResponse.created(result=new_permission.as_dict())

    except BadRequest as e:
        logger.error(f"Bad request: {e}")
        return ApiResponse.bad_request(message=str(e))
    except Exception as e:
        logger.error(f"Error creating permission: {e}")
        return ApiResponse.internal_server_error()


@permission_bp.route('/permissions/<int:permission_id>', methods=['GET'])
@inject
def get_permission_by_id(permission_id, permission_service: PermissionService):
    """
    Obtiene un permiso por su ID.
    """
    try:
        permission = permission_service.get_permission_by_id(permission_id)

        return ApiResponse.ok(result=permission.as_dict())

    except NotFound as e:
        logger.warning(f"Permission not found: {e}")
        return ApiResponse.not_found(resource="Permission", resource_id=permission_id)
    except Exception as e:
        logger.error(f"Error fetching permission by ID {permission_id}: {e}")
        return ApiResponse.internal_server_error()


@permission_bp.route('/permissions', methods=['GET'])
@inject
def get_permissions(permission_service: PermissionService):
    """
    Obtiene permisos paginados con filtros opcionales.
    
    Query parameters:
        - page: Número de página (default: 1)
        - per_page: Cantidad de resultados por página (default: 10)
        - name: Filtro opcional por nombre del permiso
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        name = request.args.get('name', type=str)

        pagination_result = permission_service.get_permissions_paginated(page, per_page, name)

        return ApiResponse.ok(**pagination_result)

    except BadRequest as e:
        logger.warning(f"Bad request: {e}")
        return ApiResponse.bad_request(message=str(e))
    except Exception as e:
        logger.error(f"Error fetching paginated permissions: {e}")
        return ApiResponse.internal_server_error()


@permission_bp.route('/permissions/<int:permission_id>', methods=['PUT'])
@inject
def update_permission(permission_id, permission_service: PermissionService):
    """
    Actualiza un permiso existente.
    
    Expected JSON body:
        {
            "name": "updated_name",
            "description": "Updated description"
        }
    """
    try:
        data = request.get_json()
        if not data:
            raise BadRequest("JSON body is required.")

        updated_permission = permission_service.update_permission(
            permission_id=permission_id,
            name=data.get('name'),
            description=data.get('description')
        )

        return ApiResponse.ok(
            result=updated_permission.as_dict(),
            message="Permission updated successfully."
        )

    except BadRequest as e:
        logger.error(f"Bad request: {e}")
        return ApiResponse.bad_request(message=str(e))
    except NotFound as e:
        logger.warning(f"Permission not found: {e}")
        return ApiResponse.not_found(resource="Permission", resource_id=permission_id)
    except Exception as e:
        logger.error(f"Error updating permission: {e}")
        return ApiResponse.internal_server_error()


@permission_bp.route('/permissions/<int:permission_id>', methods=['DELETE'])
@inject
def delete_permission(permission_id, permission_service: PermissionService):
    """
    Elimina un permiso existente por su ID.
    """
    try:
        permission_service.delete_permission(permission_id)

        return ApiResponse.ok(message="Permission deleted successfully.")

    except NotFound as e:
        logger.warning(f"Permission not found: {e}")
        return ApiResponse.not_found(resource="Permission", resource_id=permission_id)
    except Exception as e:
        logger.error(f"Error deleting permission with ID {permission_id}: {e}")
        return ApiResponse.internal_server_error()
