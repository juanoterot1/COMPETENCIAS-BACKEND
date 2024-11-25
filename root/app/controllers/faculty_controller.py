from flask import Blueprint, request
from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
from app.services.faculty_service import FacultyService
from app.utils.api_response import ApiResponse
from app.utils.jwt_decorator import jwt_required 
from app.utils.permission_decorator import requires_permission
import logging

logger = logging.getLogger(__name__)

faculty_bp = Blueprint('faculties', __name__)

@faculty_bp.route('/faculties', methods=['POST'])
@jwt_required
#@requires_permission('create_faculties') 
@inject
def create_faculty(faculty_service: FacultyService):
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            raise BadRequest("Faculty name must be provided")

        new_faculty = faculty_service.create_faculty(
            name=data.get('name'),
            id_user=data.get('id_user')
        )

        return ApiResponse.created(result=new_faculty.as_dict())

    except BadRequest as e:
        logger.error(f"Bad request: {e}")
        return ApiResponse.bad_request(message=str(e))
    except Exception as e:
        logger.error(f"Error creating faculty: {e}")
        return ApiResponse.internal_server_error()

@faculty_bp.route('/faculties/<int:faculty_id>', methods=['GET'])
@jwt_required
#@requires_permission('view_faculty')
@inject
def get_faculty_by_id(faculty_id, faculty_service: FacultyService):
    try:
        logger.info(f"Fetching faculty with ID: {faculty_id}")
        faculty = faculty_service.get_faculty_by_id(faculty_id)

        if not faculty:
            raise NotFound("Faculty not found")

        return ApiResponse.ok(result=faculty.as_dict())

    except NotFound as e:
        logger.warning(f"Faculty not found: {e}")
        return ApiResponse.not_found(resource="Faculty", resource_id=faculty_id)
    except Exception as e:
        logger.error(f"Error fetching faculty by ID {faculty_id}: {e}")
        return ApiResponse.internal_server_error()

@faculty_bp.route('/faculties', methods=['GET'])
@jwt_required
#@requires_permission('view_faculties')
@inject
def get_faculties(faculty_service: FacultyService):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        name = request.args.get('name', type=str)

        logger.info(f"Fetching faculties with filters - page: {page}, per_page: {per_page}, name: {name}")
        
        faculties, total = faculty_service.get_faculties_paginated(page, per_page, name)

        has_next = (page * per_page) < total
        has_prev = page > 1

        return ApiResponse.ok(
            result=faculties,
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
        logger.error(f"An error occurred while fetching paginated faculties: {e}")
        return ApiResponse.internal_server_error()

@faculty_bp.route('/faculties/<int:faculty_id>', methods=['PUT'])
@jwt_required
#@requires_permission('update_faculties') 
@inject
def update_faculty(faculty_id, faculty_service: FacultyService):
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            raise BadRequest("Faculty name must be provided")

        updated_faculty = faculty_service.update_faculty(
            faculty_id=faculty_id,
            name=data.get('name'),
            id_user=data.get('id_user')
        )

        if not updated_faculty:
            raise NotFound("Faculty not found")

        return ApiResponse.ok(result=updated_faculty.as_dict(), message="Faculty updated successfully.")

    except BadRequest as e:
        logger.error(f"Bad request: {e}")
        return ApiResponse.bad_request(message=str(e))
    except NotFound as e:
        logger.warning(f"Faculty not found: {e}")
        return ApiResponse.not_found(resource="Faculty", resource_id=faculty_id)
    except Exception as e:
        logger.error(f"Error updating faculty: {e}")
        return ApiResponse.internal_server_error()

@faculty_bp.route('/faculties/<int:faculty_id>', methods=['DELETE'])
@jwt_required
#@requires_permission('delete_faculties') 
@inject
def delete_faculty(faculty_id, faculty_service: FacultyService):
    try:
        logger.info(f"Deleting faculty with ID: {faculty_id}")
        deleted_faculty = faculty_service.delete_faculty(faculty_id)

        if not deleted_faculty:
            raise NotFound("Faculty not found")

        return ApiResponse.ok(message="Faculty deleted successfully.")

    except NotFound as e:
        logger.warning(f"Faculty not found: {e}")
        return ApiResponse.not_found(resource="Faculty", resource_id=faculty_id)
    except Exception as e:
        logger.error(f"Error deleting faculty with ID {faculty_id}: {e}")
        return ApiResponse.internal_server_error()