import logging
from flask_injector import inject
from werkzeug.exceptions import InternalServerError, NotFound
from app.repositories.answer_repository import AnswerRepository
from app.services.usage_log_service import UsageLogService
from app.services.question_service import QuestionService
from app.utils.sqs_utils import SQSUtils

logger = logging.getLogger(__name__)

class AnswerService:

    @inject
    def __init__(self, answer_repository: AnswerRepository, usage_log_service: UsageLogService, question_service: QuestionService):
        self.answer_repository = answer_repository
        self.usage_log_service = usage_log_service
        self.question_service = question_service

    def create_answers(self, answers_data):
        try:
            logger.info(f"Creating multiple answers. Total: {len(answers_data)}")
            new_answers = []

            for answer_data in answers_data:
                # Asegurar que cada respuesta tenga id_user = 1
                answer_data['id_user'] = answer_data.get('id_user', 1)

                new_answer = self.answer_repository.create_answer(
                    answer_description=answer_data.get('answer_description'),
                    id_evaluation=answer_data.get('id_evaluation'),
                    id_question=answer_data.get('id_question'),
                    id_user=answer_data['id_user'],  # Siempre tendrá un valor
                    score=answer_data.get('score')
                )
                new_answers.append(new_answer)

                # Registrar cada acción en el log de uso
                self.usage_log_service.create_usage_log(
                    action=f"Created answer for evaluation {answer_data.get('id_evaluation')}",
                    performed_by=answer_data['id_user']
                )

            # Preparar datos para el mensaje SQS
            string_data = ""
            for answer in new_answers:
                question = self.question_service.get_question_by_id(answer.id_question).name
                string_data += f"Descripción: {answer.answer_description}, Puntaje: {answer.score}, Pregunta: {question}\n"

            # Generar el prompt para feedback
            prompt = f"Generate feedback for the following responses: {string_data}"

            # Construir mensaje para SQS
            message_body = {
                "id_evaluation": new_answers[0].id_evaluation,
                "id_user": new_answers[0].id_user,
                "prompt_string": prompt,
                "performed_by": "system",  # Opcional, cambiar según lógica
            }

            # Enviar mensaje a SQS
            logger.info("Sending message to SQS.")
            SQSUtils.send_message(message_body)

            logger.info("Answers created and message sent to SQS.")
            return new_answers
        except Exception as e:
            logger.error(f"Error creating multiple answers: {e}")
            raise InternalServerError("An internal error occurred while creating answers.")


    def get_answer_by_id(self, answer_id, id_user=None):
        try:
            logger.info(f"Fetching answer with ID: {answer_id}")
            answer = self.answer_repository.get_answer_by_id(answer_id)

            if not answer:
                logger.info(f"Answer with ID {answer_id} not found.")
                raise NotFound("Answer not found.")

            self.usage_log_service.create_usage_log(
                action=f"Fetched answer with ID {answer_id}",
                performed_by=id_user  # Registrar el usuario que hizo la consulta
            )

            return answer
        except NotFound as e:
            logger.warning(f"Not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error fetching answer by ID {answer_id}: {e}")
            raise InternalServerError("An internal error occurred while fetching the answer.")

    def get_answers_paginated(self, page, per_page, id_evaluation=None, id_question=None):
        try:
            logger.info(f"Fetching answers with filters - page: {page}, per_page: {per_page}, id_evaluation: {id_evaluation}, id_question: {id_question}")
            answers, total = self.answer_repository.get_answers_paginated(page, per_page, id_evaluation, id_question)

            # Convertir los objetos Answer a diccionarios
            answers_as_dict = [answer.as_dict() for answer in answers]

            return answers_as_dict, total
        except Exception as e:
            logger.error(f"Error fetching paginated answers: {e}")
            raise InternalServerError("An internal error occurred while fetching paginated answers.")

    def update_answer(self, answer_id, answer_description=None, score=None, id_user=None):
        try:
            logger.info(f"Updating answer with ID: {answer_id}")
            updated_answer = self.answer_repository.update_answer(answer_id, answer_description=answer_description, score=score)

            if not updated_answer:
                logger.info(f"Answer with ID {answer_id} not found.")
                raise NotFound("Answer not found.")

            self.usage_log_service.create_usage_log(
                action=f"Updated answer with ID {answer_id}",
                performed_by=id_user  # Registrar el usuario que hizo la actualización
            )

            return updated_answer
        except NotFound as e:
            logger.warning(f"Not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error updating answer with ID {answer_id}: {e}")
            raise InternalServerError("An internal error occurred while updating the answer.")

    def delete_answer(self, answer_id, id_user=None):
        try:
            logger.info(f"Deleting answer with ID: {answer_id}")
            result = self.answer_repository.delete_answer(answer_id)

            if not result:
                logger.warning(f"Answer with ID {answer_id} not found.")
                raise NotFound(f"Answer with ID {answer_id} not found.")

            self.usage_log_service.create_usage_log(
                action=f"Deleted answer with ID {answer_id}",
                performed_by=id_user  # Registrar el usuario que eliminó la respuesta
            )

            return result
        except Exception as e:
            logger.error(f"Error deleting answer with ID {answer_id}: {e}")
            raise InternalServerError("An internal error occurred while deleting the answer.")
