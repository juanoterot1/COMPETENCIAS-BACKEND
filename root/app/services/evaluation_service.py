import logging
from flask_injector import inject
from werkzeug.exceptions import InternalServerError, NotFound
from app.repositories.evaluation_repository import EvaluationRepository
from app.services.usage_log_service import UsageLogService

logger = logging.getLogger(__name__)

class EvaluationService:

    @inject
    def __init__(self, evaluation_repository: EvaluationRepository, usage_log_service: UsageLogService):
        self.evaluation_repository = evaluation_repository
        self.usage_log_service = usage_log_service

    def create_evaluation(self, id, name, description=None, performed_by=None):
        try:
            logger.info(f"Creating a new evaluation with ID: {id} and name: {name}")
            new_evaluation = self.evaluation_repository.create_evaluation(id=id, name=name, description=description)

            self.usage_log_service.create_usage_log(
                action=f"Created evaluation with ID {id} and name {name}",
                performed_by=performed_by
            )

            return new_evaluation
        except Exception as e:
            logger.error(f"Error creating evaluation: {e}")
            raise InternalServerError("An internal error occurred while creating the evaluation.")

    def get_evaluation_by_id(self, evaluation_id, performed_by=None):
        try:
            logger.info(f"Fetching evaluation with ID: {evaluation_id}")
            evaluation = self.evaluation_repository.get_evaluation_by_id(evaluation_id)

            if not evaluation:
                logger.info(f"Evaluation with ID {evaluation_id} not found.")
                raise NotFound("Evaluation not found.")

            self.usage_log_service.create_usage_log(
                action=f"Fetched evaluation with ID {evaluation_id}",
                performed_by=performed_by
            )

            return evaluation
        except NotFound as e:
            logger.warning(f"Not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error fetching evaluation by ID {evaluation_id}: {e}")
            raise InternalServerError("An internal error occurred while fetching the evaluation.")

    def get_evaluations_paginated(self, page, per_page, name=None, description=None):
        try:
            logger.info(f"Fetching evaluations with filters - page: {page}, per_page: {per_page}, name: {name}, description: {description}")
            evaluations_query = self.evaluation_repository.get_evaluations_paginated(page, per_page, name, description)
            
            evaluations = [evaluation.as_dict() for evaluation in evaluations_query.items]
            total = evaluations_query.total
            
            return evaluations, total
        except Exception as e:
            logger.error(f"Error fetching paginated evaluations: {e}")
            raise InternalServerError("An internal error occurred while fetching paginated evaluations.")

    def update_evaluation(self, evaluation_id, name=None, description=None, performed_by=None):
        try:
            logger.info(f"Updating evaluation with ID: {evaluation_id}")
            updated_evaluation = self.evaluation_repository.update_evaluation(evaluation_id, name=name, description=description)

            if not updated_evaluation:
                logger.info(f"Evaluation with ID {evaluation_id} not found.")
                raise NotFound("Evaluation not found.")

            self.usage_log_service.create_usage_log(
                action=f"Updated evaluation with ID {evaluation_id}",
                performed_by=performed_by
            )

            return updated_evaluation
        except NotFound as e:
            logger.warning(f"Not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error updating evaluation with ID {evaluation_id}: {e}")
            raise InternalServerError("An internal error occurred while updating the evaluation.")

    def delete_evaluation(self, evaluation_id, performed_by=None):
        try:
            logger.info(f"Deleting evaluation with ID: {evaluation_id}")
            result = self.evaluation_repository.delete_evaluation(evaluation_id)

            if not result:
                logger.warning(f"Evaluation with ID {evaluation_id} not found.")
                raise NotFound(f"Evaluation with ID {evaluation_id} not found.")

            self.usage_log_service.create_usage_log(
                action=f"Deleted evaluation with ID {evaluation_id}",
                performed_by=performed_by
            )

            return result
        except Exception as e:
            logger.error(f"Error deleting evaluation with ID {evaluation_id}: {e}")
            raise InternalServerError("An internal error occurred while deleting the evaluation.")
