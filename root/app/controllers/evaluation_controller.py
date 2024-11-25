from flask import Blueprint, request
from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
from app.services.evaluation_service import EvaluationService
from app.utils.api_response import ApiResponse
from app.utils.jwt_decorator import jwt_required
from app.utils.permission_decorator import requires_permission
import logging

logger = logging.getLogger(__name__)

evaluation_bp = Blueprint('evaluations', __name__)

@evaluation_bp.route('/evaluations', methods=['POST'])
@jwt_required
#@requires_permission('create_evaluations')
@inject
def create_evaluation(evaluation_service: EvaluationService):
    try:
        data = request.get_json()
        if not data:
            raise BadRequest("Request body must be provided")

        new_evaluation = evaluation_service.create_evaluation(
            id=data.get('id'),
            name=data.get('name'),
            description=data.get('description'),
            id_subject=data.get('id_subject'),
            id_faculty=data.get('id_faculty'),
            id_user=data.get('id_user'),
            status=data.get('status')
        )

        return ApiResponse.created(result=new_evaluation.as_dict())

    except BadRequest as e:
        logger.error(f"Bad request: {e}")
        return ApiResponse.bad_request(message=str(e))
    except Exception as e:
        logger.error(f"Error creating evaluation: {e}")
        return ApiResponse.internal_server_error()


@evaluation_bp.route('/evaluations/<int:evaluation_id>', methods=['GET'])
@jwt_required
#@requires_permission('view_evaluation')
@inject
def get_evaluation_by_id(evaluation_id, evaluation_service: EvaluationService):
    try:
        logger.info(f"Fetching evaluation with ID: {evaluation_id}")
        evaluation = evaluation_service.get_evaluation_by_id(evaluation_id)

        if not evaluation:
            raise NotFound("Evaluation not found")

        return ApiResponse.ok(result=evaluation.as_dict())

    except NotFound as e:
        logger.warning(f"Evaluation not found: {e}")
        return ApiResponse.not_found(resource="Evaluation", resource_id=evaluation_id)
    except Exception as e:
        logger.error(f"Error fetching evaluation by ID {evaluation_id}: {e}")
        return ApiResponse.internal_server_error()

@evaluation_bp.route('/evaluations', methods=['GET'])
@jwt_required
#@requires_permission('view_evaluations')
@inject
def get_evaluations(evaluation_service: EvaluationService):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        name = request.args.get('name', type=str)
        description = request.args.get('description', type=str)

        logger.info(f"Fetching evaluations with filters - page: {page}, per_page: {per_page}, name: {name}, description: {description}")
        
        evaluations, total = evaluation_service.get_evaluations_paginated(page, per_page, name, description)

        has_next = (page * per_page) < total
        has_prev = page > 1

        return ApiResponse.ok(
            result=evaluations,
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
        logger.error(f"An error occurred while fetching paginated evaluations: {e}")
        return ApiResponse.internal_server_error()

@evaluation_bp.route('/evaluations/<int:evaluation_id>', methods=['PUT'])
@jwt_required
#@requires_permission('update_evaluations')
@inject
def update_evaluation(evaluation_id, evaluation_service: EvaluationService):
    try:
        data = request.get_json()
        if not data:
            raise BadRequest("Request body must be provided")

        updated_evaluation = evaluation_service.update_evaluation(
            evaluation_id=evaluation_id,
            name=data.get('name'),
            description=data.get('description'),
            id_subject=data.get('id_subject'),
            id_faculty=data.get('id_faculty'),
            id_user=data.get('id_user')
        )

        if not updated_evaluation:
            raise NotFound("Evaluation not found")

        return ApiResponse.ok(result=updated_evaluation.as_dict(), message="Evaluation updated successfully.")

    except BadRequest as e:
        logger.error(f"Bad request: {e}")
        return ApiResponse.bad_request(message=str(e))
    except NotFound as e:
        logger.warning(f"Evaluation not found: {e}")
        return ApiResponse.not_found(resource="Evaluation", resource_id=evaluation_id)
    except Exception as e:
        logger.error(f"Error updating evaluation: {e}")
        return ApiResponse.internal_server_error()

@evaluation_bp.route('/evaluations/<int:evaluation_id>', methods=['DELETE'])
@jwt_required
#@requires_permission('delete_evaluations')
@inject
def delete_evaluation(evaluation_id, evaluation_service: EvaluationService):
    try:
        logger.info(f"Deleting evaluation with ID: {evaluation_id}")
        deleted_evaluation = evaluation_service.delete_evaluation(evaluation_id)

        if not deleted_evaluation:
            raise NotFound("Evaluation not found")

        return ApiResponse.ok(message="Evaluation deleted successfully.")

    except NotFound as e:
        logger.warning(f"Evaluation not found: {e}")
        return ApiResponse.not_found(resource="Evaluation", resource_id=evaluation_id)
    except Exception as e:
        logger.error(f"Error deleting evaluation with ID {evaluation_id}: {e}")
        return ApiResponse.internal_server_error()


@evaluation_bp.route('/evaluations/count', methods=['GET'])
@jwt_required
#@requires_permission('view_evaluations')
@inject
def count_evaluations(evaluation_service: EvaluationService):
    try:
        total_evaluations = evaluation_service.count_evaluations()
        return ApiResponse.ok(result={"total_evaluations": total_evaluations})
    except Exception as e:
        logger.error(f"Error counting evaluations: {e}")
        return ApiResponse.internal_server_error()
