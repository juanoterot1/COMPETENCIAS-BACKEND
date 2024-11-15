from flask import Blueprint, request
from flask_injector import inject
from werkzeug.exceptions import BadRequest, NotFound
from app.services.answer_service import AnswerService
from app.utils.api_response import ApiResponse
from app.utils.jwt_decorator import jwt_required 
import logging

logger = logging.getLogger(__name__)

answer_bp = Blueprint('answers', __name__)

@answer_bp.route('/answers', methods=['POST'])
@jwt_required
@inject
def create_answer(answer_service: AnswerService):
    try:
        data = request.get_json()
        if not data or 'answer_description' not in data or 'id_evaluation' not in data or 'id_question' not in data or 'id_user' not in data:
            raise BadRequest("Answer description, id_evaluation, id_question and id_user must be provided")

        new_answer = answer_service.create_answer(
            answer_description=data.get('answer_description'),
            id_evaluation=data.get('id_evaluation'),
            id_question=data.get('id_question'),
            id_user=data.get('id_user'),
            score=data.get('score')
        )

        return ApiResponse.created(result=new_answer.as_dict())

    except BadRequest as e:
        logger.error(f"Bad request: {e}")
        return ApiResponse.bad_request(message=str(e))
    except Exception as e:
        logger.error(f"Error creating answer: {e}")
        return ApiResponse.internal_server_error()

@answer_bp.route('/answers/<int:answer_id>', methods=['GET'])
@jwt_required
@inject
def get_answer_by_id(answer_id, answer_service: AnswerService):
    try:
        logger.info(f"Fetching answer with ID: {answer_id}")
        answer = answer_service.get_answer_by_id(answer_id)

        if not answer:
            raise NotFound("Answer not found")

        return ApiResponse.ok(result=answer.as_dict())

    except NotFound as e:
        logger.warning(f"Answer not found: {e}")
        return ApiResponse.not_found(resource="Answer", resource_id=answer_id)
    except Exception as e:
        logger.error(f"Error fetching answer by ID {answer_id}: {e}")
        return ApiResponse.internal_server_error()

@answer_bp.route('/answers', methods=['GET'])
@jwt_required
@inject
def get_answers(answer_service: AnswerService):
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        id_evaluation = request.args.get('id_evaluation', type=int)
        id_question = request.args.get('id_question', type=int)  # Nuevo parámetro opcional

        logger.info(f"Fetching answers with filters - page: {page}, per_page: {per_page}, id_evaluation: {id_evaluation}, id_question: {id_question}")
        
        answers, total = answer_service.get_answers_paginated(page, per_page, id_evaluation, id_question)

        has_next = (page * per_page) < total
        has_prev = page > 1

        return ApiResponse.ok(
            result=answers,
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
        logger.error(f"An error occurred while fetching paginated answers: {e}")
        return ApiResponse.internal_server_error()


@answer_bp.route('/answers/<int:answer_id>', methods=['PUT'])
@jwt_required
@inject
def update_answer(answer_id, answer_service: AnswerService):
    try:
        data = request.get_json()
        if not data or 'answer_description' not in data:
            raise BadRequest("Answer description must be provided")

        updated_answer = answer_service.update_answer(
            answer_id=answer_id,
            answer_description=data.get('answer_description'),
            score=data.get('score'),
            id_user=data.get('id_user')
        )

        if not updated_answer:
            raise NotFound("Answer not found")

        return ApiResponse.ok(result=updated_answer.as_dict(), message="Answer updated successfully.")

    except BadRequest as e:
        logger.error(f"Bad request: {e}")
        return ApiResponse.bad_request(message=str(e))
    except NotFound as e:
        logger.warning(f"Answer not found: {e}")
        return ApiResponse.not_found(resource="Answer", resource_id=answer_id)
    except Exception as e:
        logger.error(f"Error updating answer: {e}")
        return ApiResponse.internal_server_error()

@answer_bp.route('/answers/<int:answer_id>', methods=['DELETE'])
@jwt_required
@inject
def delete_answer(answer_id, answer_service: AnswerService):
    try:
        logger.info(f"Deleting answer with ID: {answer_id}")
        deleted_answer = answer_service.delete_answer(answer_id)

        if not deleted_answer:
            raise NotFound("Answer not found")

        return ApiResponse.ok(message="Answer deleted successfully.")

    except NotFound as e:
        logger.warning(f"Answer not found: {e}")
        return ApiResponse.not_found(resource="Answer", resource_id=answer_id)
    except Exception as e:
        logger.error(f"Error deleting answer with ID {answer_id}: {e}")
        return ApiResponse.internal_server_error()