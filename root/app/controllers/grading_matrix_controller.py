from flask import Blueprint, request
from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
from app.services.grading_matrix_service import GradingMatrixService
from app.utils.api_response import ApiResponse
import logging

logger = logging.getLogger(__name__)

grading_matrix_bp = Blueprint('grading_matrices', __name__)

@grading_matrix_bp.route('/grading_matrices', methods=['POST'])
@inject
def create_grading_matrix(grading_matrix_service: GradingMatrixService):
    try:
        data = request.get_json()
        if not data or 'id_subject' not in data or 'total_evaluations' not in data or 'total_score' not in data or 'score' not in data:
            raise BadRequest("id_subject, total_evaluations, total_score and score must be provided")

        new_grading_matrix = grading_matrix_service.create_grading_matrix(
            id_subject=data.get('id_subject'),
            total_evaluations=data.get('total_evaluations'),
            total_score=data.get('total_score'),
            score=data.get('score'),
            recommendation=data.get('recommendation'),
            document=data.get('document'),
            id_user=data.get('id_user')
        )

        return ApiResponse.created(result=new_grading_matrix.as_dict())

    except BadRequest as e:
        logger.error(f"Bad request: {e}")
        return ApiResponse.bad_request(message=str(e))
    except Exception as e:
        logger.error(f"Error creating grading matrix: {e}")
        return ApiResponse.internal_server_error()

@grading_matrix_bp.route('/grading_matrices/<int:grading_matrix_id>', methods=['GET'])
@inject
def get_grading_matrix_by_id(grading_matrix_id, grading_matrix_service: GradingMatrixService):
    try:
        logger.info(f"Fetching grading matrix with ID: {grading_matrix_id}")
        grading_matrix = grading_matrix_service.get_grading_matrix_by_id(grading_matrix_id)

        if not grading_matrix:
            raise NotFound("Grading matrix not found")

        return ApiResponse.ok(result=grading_matrix.as_dict())

    except NotFound as e:
        logger.warning(f"Grading matrix not found: {e}")
        return ApiResponse.not_found(resource="GradingMatrix", resource_id=grading_matrix_id)
    except Exception as e:
        logger.error(f"Error fetching grading matrix by ID {grading_matrix_id}: {e}")
        return ApiResponse.internal_server_error()

@grading_matrix_bp.route('/grading_matrices', methods=['GET'])
@inject
def get_grading_matrices(grading_matrix_service: GradingMatrixService):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        id_subject = request.args.get('id_subject', type=int)

        logger.info(f"Fetching grading matrices with filters - page: {page}, per_page: {per_page}, id_subject: {id_subject}")
        
        grading_matrices, total = grading_matrix_service.get_grading_matrices_paginated(page, per_page, id_subject)

        has_next = (page * per_page) < total
        has_prev = page > 1

        return ApiResponse.ok(
            result=grading_matrices,
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
        logger.error(f"An error occurred while fetching paginated grading matrices: {e}")
        return ApiResponse.internal_server_error()

@grading_matrix_bp.route('/grading_matrices/<int:grading_matrix_id>', methods=['PUT'])
@inject
def update_grading_matrix(grading_matrix_id, grading_matrix_service: GradingMatrixService):
    try:
        data = request.get_json()
        if not data or 'total_evaluations' not in data or 'total_score' not in data or 'score' not in data:
            raise BadRequest("total_evaluations, total_score and score must be provided")

        updated_grading_matrix = grading_matrix_service.update_grading_matrix(
            grading_matrix_id=grading_matrix_id,
            total_evaluations=data.get('total_evaluations'),
            total_score=data.get('total_score'),
            score=data.get('score'),
            recommendation=data.get('recommendation'),
            document=data.get('document'),
            id_user=data.get('id_user')
        )

        if not updated_grading_matrix:
            raise NotFound("Grading matrix not found")

        return ApiResponse.ok(result=updated_grading_matrix.as_dict(), message="Grading matrix updated successfully.")

    except BadRequest as e:
        logger.error(f"Bad request: {e}")
        return ApiResponse.bad_request(message=str(e))
    except NotFound as e:
        logger.warning(f"Grading matrix not found: {e}")
        return ApiResponse.not_found(resource="GradingMatrix", resource_id=grading_matrix_id)
    except Exception as e:
        logger.error(f"Error updating grading matrix: {e}")
        return ApiResponse.internal_server_error()

@grading_matrix_bp.route('/grading_matrices/<int:grading_matrix_id>', methods=['DELETE'])
@inject
def delete_grading_matrix(grading_matrix_id, grading_matrix_service: GradingMatrixService):
    try:
        logger.info(f"Deleting grading matrix with ID: {grading_matrix_id}")
        deleted_grading_matrix = grading_matrix_service.delete_grading_matrix(grading_matrix_id)

        if not deleted_grading_matrix:
            raise NotFound("Grading matrix not found")

        return ApiResponse.ok(message="Grading matrix deleted successfully.")

    except NotFound as e:
        logger.warning(f"Grading matrix not found: {e}")
        return ApiResponse.not_found(resource="GradingMatrix", resource_id=grading_matrix_id)
    except Exception as e:
        logger.error(f"Error deleting grading matrix with ID {grading_matrix_id}: {e}")
        return ApiResponse.internal_server_error()
