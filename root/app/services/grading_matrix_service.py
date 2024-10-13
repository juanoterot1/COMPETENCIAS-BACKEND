import logging
from flask_injector import inject
from werkzeug.exceptions import InternalServerError, NotFound
from app.repositories.grading_matrix_repository import GradingMatrixRepository
from app.services.usage_log_service import UsageLogService

logger = logging.getLogger(__name__)

class GradingMatrixService:

    @inject
    def __init__(self, grading_matrix_repository: GradingMatrixRepository, usage_log_service: UsageLogService):
        self.grading_matrix_repository = grading_matrix_repository
        self.usage_log_service = usage_log_service

    def create_grading_matrix(self, id_subject, total_evaluations, total_score, score, recommendation=None, document=None, id_user=None):
        try:
            logger.info(f"Creating a new grading matrix for subject {id_subject}")
            new_grading_matrix = self.grading_matrix_repository.create_grading_matrix(
                id_subject=id_subject,
                total_evaluations=total_evaluations,
                total_score=total_score,
                score=score,
                recommendation=recommendation,
                document=document
            )

            self.usage_log_service.create_usage_log(
                action=f"Created grading matrix for subject {id_subject}",
                performed_by=id_user
            )

            return new_grading_matrix
        except Exception as e:
            logger.error(f"Error creating grading matrix: {e}")
            raise InternalServerError("An internal error occurred while creating the grading matrix.")

    def get_grading_matrix_by_id(self, grading_matrix_id, id_user=None):
        try:
            logger.info(f"Fetching grading matrix with ID: {grading_matrix_id}")
            grading_matrix = self.grading_matrix_repository.get_grading_matrix_by_id(grading_matrix_id)

            if not grading_matrix:
                logger.info(f"Grading matrix with ID {grading_matrix_id} not found.")
                raise NotFound("Grading matrix not found.")

            self.usage_log_service.create_usage_log(
                action=f"Fetched grading matrix with ID {grading_matrix_id}",
                performed_by=id_user
            )

            return grading_matrix
        except NotFound as e:
            logger.warning(f"Not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error fetching grading matrix by ID {grading_matrix_id}: {e}")
            raise InternalServerError("An internal error occurred while fetching the grading matrix.")

    def get_grading_matrices_paginated(self, page, per_page, id_subject=None):
        try:
            logger.info(f"Fetching grading matrices with filters - page: {page}, per_page: {per_page}, id_subject: {id_subject}")
            grading_matrices, total = self.grading_matrix_repository.get_grading_matrices_paginated(page, per_page, id_subject)

            # Convertir los objetos GradingMatrix a diccionarios
            grading_matrices_as_dict = [grading_matrix.as_dict() for grading_matrix in grading_matrices]

            return grading_matrices_as_dict, total
        except Exception as e:
            logger.error(f"Error fetching paginated grading matrices: {e}")
            raise InternalServerError("An internal error occurred while fetching paginated grading matrices.")

    def update_grading_matrix(self, grading_matrix_id, total_evaluations=None, total_score=None, score=None, recommendation=None, document=None, id_user=None):
        try:
            logger.info(f"Updating grading matrix with ID: {grading_matrix_id}")
            updated_grading_matrix = self.grading_matrix_repository.update_grading_matrix(
                grading_matrix_id=grading_matrix_id,
                total_evaluations=total_evaluations,
                total_score=total_score,
                score=score,
                recommendation=recommendation,
                document=document
            )

            if not updated_grading_matrix:
                logger.info(f"Grading matrix with ID {grading_matrix_id} not found.")
                raise NotFound("Grading matrix not found.")

            self.usage_log_service.create_usage_log(
                action=f"Updated grading matrix with ID {grading_matrix_id}",
                performed_by=id_user
            )

            return updated_grading_matrix
        except NotFound as e:
            logger.warning(f"Not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error updating grading matrix with ID {grading_matrix_id}: {e}")
            raise InternalServerError("An internal error occurred while updating the grading matrix.")

    def delete_grading_matrix(self, grading_matrix_id, id_user=None):
        try:
            logger.info(f"Deleting grading matrix with ID: {grading_matrix_id}")
            result = self.grading_matrix_repository.delete_grading_matrix(grading_matrix_id)

            if not result:
                logger.warning(f"Grading matrix with ID {grading_matrix_id} not found.")
                raise NotFound(f"Grading matrix with ID {grading_matrix_id} not found.")

            self.usage_log_service.create_usage_log(
                action=f"Deleted grading matrix with ID {grading_matrix_id}",
                performed_by=id_user
            )

            return result
        except Exception as e:
            logger.error(f"Error deleting grading matrix with ID {grading_matrix_id}: {e}")
            raise InternalServerError("An internal error occurred while deleting the grading matrix.")
