import logging
from flask_injector import inject
from werkzeug.exceptions import InternalServerError, NotFound
from app.repositories.subject_repository import SubjectRepository
from app.services.usage_log_service import UsageLogService

logger = logging.getLogger(__name__)

class SubjectService:

    @inject
    def __init__(self, subject_repository: SubjectRepository, usage_log_service: UsageLogService):
        self.subject_repository = subject_repository
        self.usage_log_service = usage_log_service

    def create_subject(self, name, code, id_faculty, id_user=None):
        try:
            logger.info(f"Creating a new subject with name: {name}")
            new_subject = self.subject_repository.create_subject(name=name, code=code, id_faculty=id_faculty)

            self.usage_log_service.create_usage_log(
                action=f"Created subject with name {name}",
                performed_by=id_user  # Registro del usuario que creó la materia
            )

            return new_subject
        except Exception as e:
            logger.error(f"Error creating subject: {e}")
            raise InternalServerError("An internal error occurred while creating the subject.")

    def get_subject_by_id(self, subject_id, id_user=None):
        try:
            logger.info(f"Fetching subject with ID: {subject_id}")
            subject = self.subject_repository.get_subject_by_id(subject_id)

            if not subject:
                logger.info(f"Subject with ID {subject_id} not found.")
                raise NotFound("Subject not found.")

            self.usage_log_service.create_usage_log(
                action=f"Fetched subject with ID {subject_id}",
                performed_by=id_user  # Registrar el usuario que hizo la consulta
            )

            return subject
        except NotFound as e:
            logger.warning(f"Not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error fetching subject by ID {subject_id}: {e}")
            raise InternalServerError("An internal error occurred while fetching the subject.")

    def get_subjects_paginated(self, page, per_page, name=None, code=None):
        try:
            logger.info(f"Fetching subjects with filters - page: {page}, per_page: {per_page}, name: {name}, code: {code}")
            subjects, total = self.subject_repository.get_subjects_paginated(page, per_page, name, code)

            # Convertir los subjects a diccionario si es necesario
            subjects_as_dict = [subject.as_dict() for subject in subjects]

            return subjects_as_dict, total
        except Exception as e:
            logger.error(f"Error fetching paginated subjects: {e}")
            raise InternalServerError("An internal error occurred while fetching paginated subjects.")

    def update_subject(self, subject_id, name=None, code=None, id_faculty=None, id_user=None):
        try:
            logger.info(f"Updating subject with ID: {subject_id}")
            updated_subject = self.subject_repository.update_subject(
                subject_id=subject_id,
                name=name,
                code=code,
                id_faculty=id_faculty
            )

            if not updated_subject:
                logger.info(f"Subject with ID {subject_id} not found.")
                raise NotFound("Subject not found.")

            self.usage_log_service.create_usage_log(
                action=f"Updated subject with ID {subject_id}",
                performed_by=id_user  # Registrar el usuario que hizo la actualización
            )

            return updated_subject
        except NotFound as e:
            logger.warning(f"Not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error updating subject with ID {subject_id}: {e}")
            raise InternalServerError("An internal error occurred while updating the subject.")

    def delete_subject(self, subject_id, id_user=None):
        try:
            logger.info(f"Deleting subject with ID: {subject_id}")
            result = self.subject_repository.delete_subject(subject_id)

            if not result:
                logger.warning(f"Subject with ID {subject_id} not found.")
                raise NotFound(f"Subject with ID {subject_id} not found.")

            self.usage_log_service.create_usage_log(
                action=f"Deleted subject with ID {subject_id}",
                performed_by=id_user  # Registrar el usuario que eliminó la materia
            )

            return result
        except Exception as e:
            logger.error(f"Error deleting subject with ID {subject_id}: {e}")
            raise InternalServerError("An internal error occurred while deleting the subject.")
        
    def count_subjects(self):
        try:
            logger.info("Counting total subjects")
            total_subjects = self.subject_repository.count_subjects()
            return total_subjects
        except Exception as e:
            logger.error(f"Error counting subjects: {e}")
            raise InternalServerError("An internal error occurred while counting subjects.")
