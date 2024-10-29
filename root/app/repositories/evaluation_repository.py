from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.evaluation import Evaluation

class EvaluationRepository:

    @staticmethod
    def create_evaluation(id, name, description=None, id_subject=None, id_faculty=None, id_user=None, status=None):
        """
        Crea una nueva evaluación con los campos correspondientes y la guarda en la base de datos.
        """
        try:
            new_evaluation = Evaluation(
                id=id, 
                name=name, 
                description=description, 
                id_subject=id_subject, 
                id_faculty=id_faculty, 
                id_user=id_user, 
                status=status
            )
            db.session.add(new_evaluation)
            db.session.commit()
            return new_evaluation
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_evaluation_by_id(evaluation_id):
        """
        Busca una evaluación por su ID.
        """
        try:
            return Evaluation.query.get(evaluation_id)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def get_evaluations_paginated(page, per_page, name=None, description=None):
        """
        Devuelve una lista paginada de evaluaciones, con filtros opcionales por nombre y descripción.
        """
        try:
            query = Evaluation.query
            
            # Filtrar por nombre si está presente
            if name:
                query = query.filter(Evaluation.name.ilike(f"%{name}%"))
            
            # Filtrar por descripción si está presente
            if description:
                query = query.filter(Evaluation.description.ilike(f"%{description}%"))
            
            return query.paginate(page=page, per_page=per_page, error_out=False)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def update_evaluation(evaluation_id, name=None, description=None, id_subject=None, id_faculty=None, id_user=None, status=None):
        """
        Actualiza una evaluación existente por su ID, permitiendo cambios en los campos específicos.
        """
        try:
            evaluation = Evaluation.query.get(evaluation_id)
            if evaluation is None:
                return None

            # Actualizar los campos proporcionados
            if name:
                evaluation.name = name
            if description:
                evaluation.description = description
            if id_subject:
                evaluation.id_subject = id_subject
            if id_faculty:
                evaluation.id_faculty = id_faculty
            if id_user:
                evaluation.id_user = id_user
            if status:
                evaluation.status = status

            db.session.commit()
            return evaluation
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_evaluation(evaluation_id):
        """
        Elimina una evaluación por su ID.
        """
        try:
            evaluation = Evaluation.query.get(evaluation_id)
            if evaluation is None:
                return None

            db.session.delete(evaluation)
            db.session.commit()
            return evaluation
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def count_evaluations():
        """
        Cuenta el número total de evaluaciones en la base de datos.
        """
        try:
            return Evaluation.query.count()
        except SQLAlchemyError as e:
            raise e
