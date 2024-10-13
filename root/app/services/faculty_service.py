import logging
from flask_injector import inject
from werkzeug.exceptions import InternalServerError, NotFound
from app.repositories.faculty_repository import FacultyRepository
from app.services.usage_log_service import UsageLogService

logger = logging.getLogger(__name__)

class FacultyService:

    @inject
    def __init__(self, faculty_repository: FacultyRepository, usage_log_service: UsageLogService):
        self.faculty_repository = faculty_repository
        self.usage_log_service = usage_log_service

    def create_faculty(self, name, id_user=None):
        try:
            logger.info(f"Creating a new faculty with name: {name}")
            new_faculty = self.faculty_repository.create_faculty(name=name)

            self.usage_log_service.create_usage_log(
                action=f"Created faculty with name {name}",
                performed_by=id_user  # Registrar el usuario que creó la facultad
            )

            return new_faculty
        except Exception as e:
            logger.error(f"Error creating faculty: {e}")
            raise InternalServerError("An internal error occurred while creating the faculty.")

    def get_faculty_by_id(self, faculty_id, id_user=None):
        try:
            logger.info(f"Fetching faculty with ID: {faculty_id}")
            faculty = self.faculty_repository.get_faculty_by_id(faculty_id)

            if not faculty:
                logger.info(f"Faculty with ID {faculty_id} not found.")
                raise NotFound("Faculty not found.")

            self.usage_log_service.create_usage_log(
                action=f"Fetched faculty with ID {faculty_id}",
                performed_by=id_user  # Registrar el usuario que hizo la consulta
            )

            return faculty
        except NotFound as e:
            logger.warning(f"Not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error fetching faculty by ID {faculty_id}: {e}")
            raise InternalServerError("An internal error occurred while fetching the faculty.")

    def get_faculties_paginated(self, page, per_page, name=None):
        try:
            logger.info(f"Fetching faculties with filters - page: {page}, per_page: {per_page}, name: {name}")
            faculties, total = self.faculty_repository.get_faculties_paginated(page, per_page, name)

            # Convertir los objetos Faculty a diccionarios
            faculties_as_dict = [faculty.as_dict() for faculty in faculties]

            return faculties_as_dict, total
        except Exception as e:
            logger.error(f"Error fetching paginated faculties: {e}")
            raise InternalServerError("An internal error occurred while fetching paginated faculties.")

    def update_faculty(self, faculty_id, name=None, id_user=None):
        try:
            logger.info(f"Updating faculty with ID: {faculty_id}")
            updated_faculty = self.faculty_repository.update_faculty(faculty_id, name=name)

            if not updated_faculty:
                logger.info(f"Faculty with ID {faculty_id} not found.")
                raise NotFound("Faculty not found.")

            self.usage_log_service.create_usage_log(
                action=f"Updated faculty with ID {faculty_id}",
                performed_by=id_user  # Registrar el usuario que hizo la actualización
            )

            return updated_faculty
        except NotFound as e:
            logger.warning(f"Not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error updating faculty with ID {faculty_id}: {e}")
            raise InternalServerError("An internal error occurred while updating the faculty.")

    def delete_faculty(self, faculty_id, id_user=None):
        try:
            logger.info(f"Deleting faculty with ID: {faculty_id}")
            result = self.faculty_repository.delete_faculty(faculty_id)

            if not result:
                logger.warning(f"Faculty with ID {faculty_id} not found.")
                raise NotFound(f"Faculty with ID {faculty_id} not found.")

            self.usage_log_service.create_usage_log(
                action=f"Deleted faculty with ID {faculty_id}",
                performed_by=id_user  # Registrar el usuario que eliminó la facultad
            )

            return result
        except Exception as e:
            logger.error(f"Error deleting faculty with ID {faculty_id}: {e}")
            raise InternalServerError("An internal error occurred while deleting the faculty.")
