from flask import Blueprint, request
from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
from app.services.subject_service import SubjectService
from app.utils.api_response import ApiResponse
from app.utils.jwt_decorator import jwt_required
import logging

logger = logging.getLogger(__name__)

subject_bp = Blueprint('subjects', __name__)

@subject_bp.route('/subjects', methods=['POST'])
@jwt_required
@inject
def create_subject(subject_service: SubjectService):
    try:
        data = request.get_json()
        if not data or 'name' not in data or 'id_faculty' not in data:
            raise BadRequest("Subject name and id_faculty must be provided")

        new_subject = subject_service.create_subject(
            name=data.get('name'),
            code=data.get('code'),
            id_faculty=data.get('id_faculty'),
            id_user=data.get('id_user')
        )

        return ApiResponse.created(result=new_subject.as_dict())

    except BadRequest as e:
        logger.error(f"Bad request: {e}")
        return ApiResponse.bad_request(message=str(e))
    except Exception as e:
        logger.error(f"Error creating subject: {e}")
        return ApiResponse.internal_server_error()

@subject_bp.route('/subjects/<int:subject_id>', methods=['GET'])
@jwt_required
@inject
def get_subject_by_id(subject_id, subject_service: SubjectService):
    try:
        logger.info(f"Fetching subject with ID: {subject_id}")
        subject = subject_service.get_subject_by_id(subject_id)

        if not subject:
            raise NotFound("Subject not found")

        return ApiResponse.ok(result=subject.as_dict())

    except NotFound as e:
        logger.warning(f"Subject not found: {e}")
        return ApiResponse.not_found(resource="Subject", resource_id=subject_id)
    except Exception as e:
        logger.error(f"Error fetching subject by ID {subject_id}: {e}")
        return ApiResponse.internal_server_error()

@subject_bp.route('/subjects', methods=['GET'])
@jwt_required
@inject
def get_subjects(subject_service: SubjectService):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        name = request.args.get('name', type=str)
        code = request.args.get('code', type=str)

        logger.info(f"Fetching subjects with filters - page: {page}, per_page: {per_page}, name: {name}, code: {code}")
        
        subjects, total = subject_service.get_subjects_paginated(page, per_page, name, code)

        has_next = (page * per_page) < total
        has_prev = page > 1

        return ApiResponse.ok(
            result=subjects,
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
        logger.error(f"An error occurred while fetching paginated subjects: {e}")
        return ApiResponse.internal_server_error()

@subject_bp.route('/subjects/<int:subject_id>', methods=['PUT'])
@jwt_required
@inject
def update_subject(subject_id, subject_service: SubjectService):
    try:
        data = request.get_json()
        if not data or 'name' not in data or 'id_faculty' not in data:
            raise BadRequest("Subject name and id_faculty must be provided")

        updated_subject = subject_service.update_subject(
            subject_id=subject_id,
            name=data.get('name'),
            code=data.get('code'),
            id_faculty=data.get('id_faculty'),
            id_user=data.get('id_user')
        )

        if not updated_subject:
            raise NotFound("Subject not found")

        return ApiResponse.ok(result=updated_subject.as_dict(), message="Subject updated successfully.")

    except BadRequest as e:
        logger.error(f"Bad request: {e}")
        return ApiResponse.bad_request(message=str(e))
    except NotFound as e:
        logger.warning(f"Subject not found: {e}")
        return ApiResponse.not_found(resource="Subject", resource_id=subject_id)
    except Exception as e:
        logger.error(f"Error updating subject: {e}")
        return ApiResponse.internal_server_error()

@subject_bp.route('/subjects/<int:subject_id>', methods=['DELETE'])
@jwt_required
@inject
def delete_subject(subject_id, subject_service: SubjectService):
    try:
        logger.info(f"Deleting subject with ID: {subject_id}")
        deleted_subject = subject_service.delete_subject(subject_id)

        if not deleted_subject:
            raise NotFound("Subject not found")

        return ApiResponse.ok(message="Subject deleted successfully.")

    except NotFound as e:
        logger.warning(f"Subject not found: {e}")
        return ApiResponse.not_found(resource="Subject", resource_id=subject_id)
    except Exception as e:
        logger.error(f"Error deleting subject with ID {subject_id}: {e}")
        return ApiResponse.internal_server_error()

@subject_bp.route('/subjects/count', methods=['GET'])
@inject
def count_subjects(subject_service: SubjectService):
    try:
        total_subjects = subject_service.count_subjects()
        return ApiResponse.ok(result={"total_subjects": total_subjects})
    except Exception as e:
        logger.error(f"Error counting subjects: {e}")
        return ApiResponse.internal_server_error()