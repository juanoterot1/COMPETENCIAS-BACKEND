from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.grading_matrix import GradingMatrix

class GradingMatrixRepository:

    @staticmethod
    def create_grading_matrix(id_subject, total_evaluations, total_score, score, recommendation=None, document=None):
        """
        Crea una nueva GradingMatrix y la guarda en la base de datos.
        """
        try:
            new_grading_matrix = GradingMatrix(
                id_subject=id_subject,
                total_evaluations=total_evaluations,
                total_score=total_score,
                score=score,
                recommendation=recommendation,
                document=document
            )
            db.session.add(new_grading_matrix)
            db.session.commit()
            return new_grading_matrix
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_grading_matrix_by_id(grading_matrix_id):
        """
        Busca una GradingMatrix por su ID.
        """
        try:
            return GradingMatrix.query.get(grading_matrix_id)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def get_grading_matrices_paginated(page, per_page, id_subject=None):
        """
        Devuelve una lista paginada de GradingMatrices, con filtro opcional por id_subject.
        """
        try:
            query = GradingMatrix.query
            
            # Filtrar por subject si está presente
            if id_subject:
                query = query.filter(GradingMatrix.id_subject == id_subject)
            
            return query.paginate(page=page, per_page=per_page, error_out=False)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def update_grading_matrix(grading_matrix_id, total_evaluations=None, total_score=None, score=None, recommendation=None, document=None):
        """
        Actualiza una GradingMatrix existente por su ID.
        """
        try:
            grading_matrix = GradingMatrix.query.get(grading_matrix_id)
            if grading_matrix is None:
                return None

            # Actualizar los campos proporcionados
            if total_evaluations:
                grading_matrix.total_evaluations = total_evaluations
            if total_score:
                grading_matrix.total_score = total_score
            if score:
                grading_matrix.score = score
            if recommendation:
                grading_matrix.recommendation = recommendation
            if document:
                grading_matrix.document = document

            db.session.commit()
            return grading_matrix
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_grading_matrix(grading_matrix_id):
        """
        Elimina una GradingMatrix por su ID.
        """
        try:
            grading_matrix = GradingMatrix.query.get(grading_matrix_id)
            if grading_matrix is None:
                return None

            db.session.delete(grading_matrix)
            db.session.commit()
            return grading_matrix
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
