import logging
from flask_injector import inject
from werkzeug.exceptions import InternalServerError, NotFound
from app.repositories.question_repository import QuestionRepository
from app.services.usage_log_service import UsageLogService

logger = logging.getLogger(__name__)

class QuestionService:

    @inject
    def __init__(self, question_repository: QuestionRepository, usage_log_service: UsageLogService):
        self.question_repository = question_repository
        self.usage_log_service = usage_log_service

    def create_question(self, name, value, id_evaluation, id_user=None):
        try:
            logger.info(f"Creating a new question with name: {name}")
            new_question = self.question_repository.create_question(name=name, value=value, id_evaluation=id_evaluation)

            self.usage_log_service.create_usage_log(
                action=f"Created question with name {name}",
                performed_by=id_user  # Registrar el usuario que creó la pregunta
            )

            return new_question
        except Exception as e:
            logger.error(f"Error creating question: {e}")
            raise InternalServerError("An internal error occurred while creating the question.")

    def get_question_by_id(self, question_id, id_user=None):
        try:
            logger.info(f"Fetching question with ID: {question_id}")
            question = self.question_repository.get_question_by_id(question_id)

            if not question:
                logger.info(f"Question with ID {question_id} not found.")
                raise NotFound("Question not found.")

            self.usage_log_service.create_usage_log(
                action=f"Fetched question with ID {question_id}",
                performed_by=id_user  # Registrar el usuario que hizo la consulta
            )

            return question
        except NotFound as e:
            logger.warning(f"Not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error fetching question by ID {question_id}: {e}")
            raise InternalServerError("An internal error occurred while fetching the question.")

    def get_questions_paginated(self, page, per_page, name=None):
        try:
            logger.info(f"Fetching questions with filters - page: {page}, per_page: {per_page}, name: {name}")
            questions, total = self.question_repository.get_questions_paginated(page, per_page, name)

            # Convertir las preguntas a diccionario si es necesario
            questions_as_dict = [question.as_dict() for question in questions]

            return questions_as_dict, total
        except Exception as e:
            logger.error(f"Error fetching paginated questions: {e}")
            raise InternalServerError("An internal error occurred while fetching paginated questions.")

    def update_question(self, question_id, name=None, value=None, id_evaluation=None, id_user=None):
        try:
            logger.info(f"Updating question with ID: {question_id}")
            updated_question = self.question_repository.update_question(question_id, name=name, value=value, id_evaluation=id_evaluation)

            if not updated_question:
                logger.info(f"Question with ID {question_id} not found.")
                raise NotFound("Question not found.")

            self.usage_log_service.create_usage_log(
                action=f"Updated question with ID {question_id}",
                performed_by=id_user  # Registrar el usuario que hizo la actualización
            )

            return updated_question
        except NotFound as e:
            logger.warning(f"Not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error updating question with ID {question_id}: {e}")
            raise InternalServerError("An internal error occurred while updating the question.")

    def delete_question(self, question_id, id_user=None):
        try:
            logger.info(f"Deleting question with ID: {question_id}")
            result = self.question_repository.delete_question(question_id)

            if not result:
                logger.warning(f"Question with ID {question_id} not found.")
                raise NotFound(f"Question with ID {question_id} not found.")

            self.usage_log_service.create_usage_log(
                action=f"Deleted question with ID {question_id}",
                performed_by=id_user  # Registrar el usuario que eliminó la pregunta
            )

            return result
        except Exception as e:
            logger.error(f"Error deleting question with ID {question_id}: {e}")
            raise InternalServerError("An internal error occurred while deleting the question.")
