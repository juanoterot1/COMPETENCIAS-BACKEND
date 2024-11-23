import logging
from flask_injector import inject
from werkzeug.exceptions import InternalServerError, NotFound, BadRequest
from app.repositories.feedback_repository import FeedbackRepository
from app.services.usage_log_service import UsageLogService

logger = logging.getLogger(__name__)

class FeedbackService:

    @inject
    def __init__(self, feedback_repository: FeedbackRepository, usage_log_service: UsageLogService):
        self.feedback_repository = feedback_repository
        self.usage_log_service = usage_log_service

    def create_feedback(self, id_evaluation, id_user, feedback_text, performed_by=None):
        """
        Crea un nuevo registro de feedback.
        
        Parameters:
            id_evaluation (int): ID de la evaluación relacionada.
            id_user (int): ID del usuario que proporciona el feedback.
            feedback_text (str): Texto de la retroalimentación.
            performed_by (int, optional): ID del usuario que realiza la acción.
        
        Returns:
            Feedback: El objeto de feedback creado.
        """
        try:
            logger.info(f"Creating feedback for evaluation ID {id_evaluation} by user ID {id_user}")
            new_feedback = self.feedback_repository.create_feedback(
                id_evaluation=id_evaluation,
                id_user=id_user,
                feedback_text=feedback_text
            )

            self.usage_log_service.create_usage_log(
                action=f"Created feedback for evaluation ID {id_evaluation} by user ID {id_user}",
                performed_by=performed_by
            )

            return new_feedback
        except Exception as e:
            logger.error(f"Error creating feedback: {e}")
            raise InternalServerError("An internal error occurred while creating the feedback.")

    def get_feedback_by_id(self, feedback_id, performed_by=None):
        """
        Obtiene un registro de feedback por su ID.
        
        Parameters:
            feedback_id (int): ID del feedback.
            performed_by (int, optional): ID del usuario que realiza la acción.
        
        Returns:
            Feedback: El objeto de feedback si se encuentra.
        """
        try:
            logger.info(f"Fetching feedback with ID {feedback_id}")
            feedback = self.feedback_repository.get_feedback_by_id(feedback_id)

            if not feedback:
                logger.info(f"Feedback with ID {feedback_id} not found.")
                raise NotFound("Feedback not found.")

            self.usage_log_service.create_usage_log(
                action=f"Fetched feedback with ID {feedback_id}",
                performed_by=performed_by
            )

            return feedback
        except NotFound as e:
            logger.warning(f"Not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error fetching feedback with ID {feedback_id}: {e}")
            raise InternalServerError("An internal error occurred while fetching the feedback.")

    def get_feedbacks_by_evaluation(self, evaluation_id):
        """
        Obtiene todos los feedbacks relacionados con una evaluación específica.
        
        Parameters:
            evaluation_id (int): ID de la evaluación.
        
        Returns:
            List[Feedback]: Lista de objetos de feedback.
        """
        try:
            logger.info(f"Fetching feedbacks for evaluation ID {evaluation_id}")
            feedbacks = self.feedback_repository.get_feedbacks_by_evaluation(evaluation_id)
            return [feedback.as_dict() for feedback in feedbacks]
        except Exception as e:
            logger.error(f"Error fetching feedbacks for evaluation ID {evaluation_id}: {e}")
            raise InternalServerError("An internal error occurred while fetching feedbacks.")

    def update_feedback(self, feedback_id, feedback_text=None, performed_by=None):
        """
        Actualiza un registro de feedback existente.
        
        Parameters:
            feedback_id (int): ID del feedback a actualizar.
            feedback_text (str, optional): Nuevo texto de retroalimentación.
            performed_by (int, optional): ID del usuario que realiza la acción.
        
        Returns:
            Feedback: El objeto de feedback actualizado.
        """
        try:
            logger.info(f"Updating feedback with ID {feedback_id}")
            updated_feedback = self.feedback_repository.update_feedback(
                feedback_id=feedback_id,
                feedback_text=feedback_text
            )

            if not updated_feedback:
                logger.info(f"Feedback with ID {feedback_id} not found.")
                raise NotFound("Feedback not found.")

            self.usage_log_service.create_usage_log(
                action=f"Updated feedback with ID {feedback_id}",
                performed_by=performed_by
            )

            return updated_feedback
        except NotFound as e:
            logger.warning(f"Not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error updating feedback with ID {feedback_id}: {e}")
            raise InternalServerError("An internal error occurred while updating the feedback.")

    def delete_feedback(self, feedback_id, performed_by=None):
        """
        Elimina un registro de feedback por su ID.
        
        Parameters:
            feedback_id (int): ID del feedback a eliminar.
            performed_by (int, optional): ID del usuario que realiza la acción.
        
        Returns:
            Feedback: El objeto de feedback eliminado.
        """
        try:
            logger.info(f"Deleting feedback with ID {feedback_id}")
            deleted_feedback = self.feedback_repository.delete_feedback(feedback_id)

            if not deleted_feedback:
                logger.info(f"Feedback with ID {feedback_id} not found.")
                raise NotFound("Feedback not found.")

            self.usage_log_service.create_usage_log(
                action=f"Deleted feedback with ID {feedback_id}",
                performed_by=performed_by
            )

            return deleted_feedback
        except NotFound as e:
            logger.warning(f"Not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error deleting feedback with ID {feedback_id}: {e}")
            raise InternalServerError("An internal error occurred while deleting the feedback.")

    def get_feedbacks_paginated(self, page, per_page, id_evaluation=None, id_user=None):
        """
        Obtiene feedbacks paginados con filtros opcionales.
        
        Parameters:
            page (int): Número de página.
            per_page (int): Número de registros por página.
            id_evaluation (int, optional): Filtrar por ID de evaluación.
            id_user (int, optional): Filtrar por ID de usuario.
        
        Returns:
            tuple: (feedbacks, total)
        """
        try:
            logger.info(f"Fetching paginated feedbacks - page: {page}, per_page: {per_page}")
            feedbacks_query = self.feedback_repository.get_feedbacks_paginated(page, per_page, id_evaluation, id_user)

            feedbacks = [feedback.as_dict() for feedback in feedbacks_query.items]
            total = feedbacks_query.total

            return feedbacks, total  # Devolver feedbacks y total por separado
        except Exception as e:
            logger.error(f"Error fetching paginated feedbacks: {e}")
            raise InternalServerError("An internal error occurred while fetching paginated feedbacks.")