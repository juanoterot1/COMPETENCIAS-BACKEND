from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.faculties import Faculty

class FacultyRepository:

    @staticmethod
    def create_faculty(name):
        """
        Crea una nueva facultad y la guarda en la base de datos.
        """
        try:
            new_faculty = Faculty(name=name)
            db.session.add(new_faculty)
            db.session.commit()
            return new_faculty
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_faculty_by_id(faculty_id):
        """
        Busca una facultad por su ID.
        """
        try:
            return Faculty.query.get(faculty_id)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def get_faculties_paginated(page, per_page, name=None):
        """
        Devuelve una lista paginada de facultades, con un filtro opcional por nombre.
        """
        try:
            query = Faculty.query

            # Filtrar por nombre si está presente
            if name:
                query = query.filter(Faculty.name.ilike(f"%{name}%"))

            # Usar paginate de SQLAlchemy
            paginated_faculties = query.paginate(page=page, per_page=per_page, error_out=False)

            # Devolver los items y el total de la paginación
            return paginated_faculties.items, paginated_faculties.total
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def update_faculty(faculty_id, name=None):
        """
        Actualiza una facultad existente por su ID.
        """
        try:
            faculty = Faculty.query.get(faculty_id)
            if faculty is None:
                return None

            # Actualizar los campos proporcionados
            if name:
                faculty.name = name

            db.session.commit()
            return faculty
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_faculty(faculty_id):
        """
        Elimina una facultad por su ID.
        """
        try:
            faculty = Faculty.query.get(faculty_id)
            if faculty is None:
                return None

            db.session.delete(faculty)
            db.session.commit()
            return faculty
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
