from flask import Blueprint, request
from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
from app.services.question_service import QuestionService
from app.utils.api_response import ApiResponse
from app.utils.jwt_decorator import jwt_required
from app.utils.permission_decorator import requires_permission
import logging

logger = logging.getLogger(__name__)

question_bp = Blueprint('questions', __name__)

@question_bp.route('/questions', methods=['POST'])
@jwt_required
#@requires_permission('create_questions')
@inject
def create_question(question_service: QuestionService):
    try:
        data = request.get_json()
        if not data or 'name' not in data or 'value' not in data or 'id_evaluation' not in data:
            raise BadRequest("Question name, value and id_evaluation must be provided")

        new_question = question_service.create_question(
            name=data.get('name'),
            value=data.get('value'),
            id_evaluation=data.get('id_evaluation'),
            id_user=data.get('id_user')
        )

        return ApiResponse.created(result=new_question.as_dict())

    except BadRequest as e:
        logger.error(f"Bad request: {e}")
        return ApiResponse.bad_request(message=str(e))
    except Exception as e:
        logger.error(f"Error creating question: {e}")
        return ApiResponse.internal_server_error()

@question_bp.route('/questions/<int:question_id>', methods=['GET'])
@jwt_required
#@requires_permission('view_question')
@inject
def get_question_by_id(question_id, question_service: QuestionService):
    try:
        logger.info(f"Fetching question with ID: {question_id}")
        question = question_service.get_question_by_id(question_id)

        if not question:
            raise NotFound("Question not found")

        return ApiResponse.ok(result=question.as_dict())

    except NotFound as e:
        logger.warning(f"Question not found: {e}")
        return ApiResponse.not_found(resource="Question", resource_id=question_id)
    except Exception as e:
        logger.error(f"Error fetching question by ID {question_id}: {e}")
        return ApiResponse.internal_server_error()

@question_bp.route('/questions', methods=['GET'])
@jwt_required
#@requires_permission('view_questions')
@inject
def get_questions(question_service: QuestionService):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        name = request.args.get('name', type=str)

        logger.info(f"Fetching questions with filters - page: {page}, per_page: {per_page}, name: {name}")
        
        questions, total = question_service.get_questions_paginated(page, per_page, name)

        has_next = (page * per_page) < total
        has_prev = page > 1

        return ApiResponse.ok(
            result=questions,
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
        logger.error(f"An error occurred while fetching paginated questions: {e}")
        return ApiResponse.internal_server_error()

@question_bp.route('/questions/<int:question_id>', methods=['PUT'])
@jwt_required
#@requires_permission('update_questions')
@inject
def update_question(question_id, question_service: QuestionService):
    try:
        data = request.get_json()
        if not data or 'name' not in data or 'value' not in data or 'id_evaluation' not in data:
            raise BadRequest("Question name, value and id_evaluation must be provided")

        updated_question = question_service.update_question(
            question_id=question_id,
            name=data.get('name'),
            value=data.get('value'),
            id_evaluation=data.get('id_evaluation'),
            id_user=data.get('id_user')
        )

        if not updated_question:
            raise NotFound("Question not found")

        return ApiResponse.ok(result=updated_question.as_dict(), message="Question updated successfully.")

    except BadRequest as e:
        logger.error(f"Bad request: {e}")
        return ApiResponse.bad_request(message=str(e))
    except NotFound as e:
        logger.warning(f"Question not found: {e}")
        return ApiResponse.not_found(resource="Question", resource_id=question_id)
    except Exception as e:
        logger.error(f"Error updating question: {e}")
        return ApiResponse.internal_server_error()

@question_bp.route('/questions/<int:question_id>', methods=['DELETE'])
@jwt_required
#@requires_permission('delete_questions')
@inject
def delete_question(question_id, question_service: QuestionService):
    try:
        logger.info(f"Deleting question with ID: {question_id}")
        deleted_question = question_service.delete_question(question_id)

        if not deleted_question:
            raise NotFound("Question not found")

        return ApiResponse.ok(message="Question deleted successfully.")

    except NotFound as e:
        logger.warning(f"Question not found: {e}")
        return ApiResponse.not_found(resource="Question", resource_id=question_id)
    except Exception as e:
        logger.error(f"Error deleting question with ID {question_id}: {e}")
        return ApiResponse.internal_server_error()
