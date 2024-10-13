from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.subjects import Subject

class SubjectRepository:

    @staticmethod
    def create_subject(name, code, id_faculty):
        """
        Crea una nueva materia y la guarda en la base de datos.
        """
        try:
            new_subject = Subject(name=name, code=code, id_faculty=id_faculty)
            db.session.add(new_subject)
            db.session.commit()
            return new_subject
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_subject_by_id(subject_id):
        """
        Busca una materia por su ID.
        """
        try:
            return Subject.query.get(subject_id)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def get_subjects_paginated(page, per_page, name=None, code=None):
        """
        Devuelve una lista paginada de materias, con filtros opcionales por nombre o código.
        """
        try:
            query = Subject.query
            
            # Filtrar por nombre si está presente
            if name:
                query = query.filter(Subject.name.ilike(f"%{name}%"))
            
            # Filtrar por código si está presente
            if code:
                query = query.filter(Subject.code.ilike(f"%{code}%"))
            
            # Usar paginate de SQLAlchemy
            paginated_subjects = query.paginate(page=page, per_page=per_page, error_out=False)

            # Devolver los items y el total de la paginación
            return paginated_subjects.items, paginated_subjects.total
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def update_subject(subject_id, name=None, code=None, id_faculty=None):
        """
        Actualiza una materia existente por su ID.
        """
        try:
            subject = Subject.query.get(subject_id)
            if subject is None:
                return None

            # Actualizar los campos proporcionados
            if name:
                subject.name = name
            if code:
                subject.code = code
            if id_faculty:
                subject.id_faculty = id_faculty

            db.session.commit()
            return subject
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_subject(subject_id):
        """
        Elimina una materia por su ID.
        """
        try:
            subject = Subject.query.get(subject_id)
            if subject is None:
                return None

            db.session.delete(subject)
            db.session.commit()
            return subject
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
