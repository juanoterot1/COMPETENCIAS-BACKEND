from flask import Blueprint, request
from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
from app.services.feedback_service import FeedbackService
from app.utils.api_response import ApiResponse
from app.utils.jwt_decorator import jwt_required
from app.utils.permission_decorator import requires_permission
import logging

logger = logging.getLogger(__name__)

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback', methods=['POST'])
@jwt_required
# @requires_permission('create_feedback')
@inject
def create_feedback(feedback_service: FeedbackService):
    """
    Endpoint para crear un nuevo feedback.
    """
    try:
        data = request.get_json()
        if not data:
            raise BadRequest("Request body must be provided")

        new_feedback = feedback_service.create_feedback(
            id_evaluation=data.get('id_evaluation'),
            id_user=data.get('id_user'),
            feedback_text=data.get('feedback_text'),
            performed_by=data.get('performed_by')
        )

        return ApiResponse.created(result=new_feedback.as_dict())

    except BadRequest as e:
        logger.error(f"Bad request: {e}")
        return ApiResponse.bad_request(message=str(e))
    except Exception as e:
        logger.error(f"Error creating feedback: {e}")
        return ApiResponse.internal_server_error()

@feedback_bp.route('/feedback', methods=['GET'])
@jwt_required
# @requires_permission('view_feedbacks')
@inject
def get_feedbacks(feedback_service: FeedbackService):
    """
    Retrieves a paginated list of feedbacks with optional filters.
    
    Query Params:
        page (int): The page number to retrieve.
        per_page (int): The number of feedbacks per page.
        id_evaluation (int): Filter by evaluation ID.
        id_user (int): Filter by user ID.

    Returns:
        Response: JSON response with paginated feedbacks or error message.
    """
    try:
        # Extract query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        id_evaluation = request.args.get('id_evaluation', type=int)
        id_user = request.args.get('id_user', type=int)

        logger.info(f"Fetching feedbacks with filters - page: {page}, per_page: {per_page}, id_evaluation: {id_evaluation}, id_user: {id_user}")

        # Fetch paginated feedbacks
        feedbacks, total = feedback_service.get_feedbacks_paginated(page, per_page, id_evaluation, id_user)

        # Determine pagination details
        has_next = (page * per_page) < total
        has_prev = page > 1

        return ApiResponse.ok(
            result=feedbacks,
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
        logger.error(f"An error occurred while fetching paginated feedbacks: {e}")
        return ApiResponse.internal_server_error()
    
    
@feedback_bp.route('/feedback/<int:feedback_id>', methods=['GET'])
@jwt_required
# @requires_permission('view_feedback')
@inject
def get_feedback_by_id(feedback_id, feedback_service: FeedbackService):
    """
    Endpoint para obtener un feedback por ID.
    """
    try:
        logger.info(f"Fetching feedback with ID: {feedback_id}")
        feedback = feedback_service.get_feedback_by_id(feedback_id)

        if not feedback:
            raise NotFound("Feedback not found")

        return ApiResponse.ok(result=feedback.as_dict())

    except NotFound as e:
        logger.warning(f"Feedback not found: {e}")
        return ApiResponse.not_found(resource="Feedback", resource_id=feedback_id)
    except Exception as e:
        logger.error(f"Error fetching feedback with ID {feedback_id}: {e}")
        return ApiResponse.internal_server_error()

@feedback_bp.route('/feedback/<int:feedback_id>', methods=['PUT'])
@jwt_required
# @requires_permission('update_feedback')
@inject
def update_feedback(feedback_id, feedback_service: FeedbackService):
    """
    Endpoint para actualizar un feedback por ID.
    """
    try:
        data = request.get_json()
        if not data:
            raise BadRequest("Request body must be provided")

        updated_feedback = feedback_service.update_feedback(
            feedback_id=feedback_id,
            feedback_text=data.get('feedback_text'),
            performed_by=data.get('performed_by')
        )

        if not updated_feedback:
            raise NotFound("Feedback not found")

        return ApiResponse.ok(result=updated_feedback.as_dict(), message="Feedback updated successfully.")

    except BadRequest as e:
        logger.error(f"Bad request: {e}")
        return ApiResponse.bad_request(message=str(e))
    except NotFound as e:
        logger.warning(f"Feedback not found: {e}")
        return ApiResponse.not_found(resource="Feedback", resource_id=feedback_id)
    except Exception as e:
        logger.error(f"Error updating feedback: {e}")
        return ApiResponse.internal_server_error()

@feedback_bp.route('/feedback/<int:feedback_id>', methods=['DELETE'])
@jwt_required
# @requires_permission('delete_feedback')
@inject
def delete_feedback(feedback_id, feedback_service: FeedbackService):
    """
    Endpoint para eliminar un feedback por ID.
    """
    try:
        logger.info(f"Deleting feedback with ID: {feedback_id}")
        deleted_feedback = feedback_service.delete_feedback(feedback_id)

        if not deleted_feedback:
            raise NotFound("Feedback not found")

        return ApiResponse.ok(message="Feedback deleted successfully.")

    except NotFound as e:
        logger.warning(f"Feedback not found: {e}")
        return ApiResponse.not_found(resource="Feedback", resource_id=feedback_id)
    except Exception as e:
        logger.error(f"Error deleting feedback with ID {feedback_id}: {e}")
        return ApiResponse.internal_server_error()
