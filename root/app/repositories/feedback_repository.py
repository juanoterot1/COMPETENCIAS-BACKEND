from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.feedback import Feedback

class FeedbackRepository:

    @staticmethod
    def create_feedback(id_evaluation, id_user, feedback_text):
        """
        Crea un nuevo registro de feedback en la base de datos.
        
        Parameters:
            id_evaluation (int): ID de la evaluación relacionada.
            id_user (int): ID del usuario que proporciona el feedback.
            feedback_text (str): Texto de la retroalimentación.
        
        Returns:
            Feedback: El objeto de feedback recién creado.
        """
        try:
            new_feedback = Feedback(
                id_evaluation=id_evaluation,
                id_user=id_user,
                feedback_text=feedback_text
            )
            db.session.add(new_feedback)
            db.session.commit()
            return new_feedback
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_feedback_by_id(feedback_id):
        """
        Obtiene un registro de feedback por su ID.
        
        Parameters:
            feedback_id (int): ID del feedback.
        
        Returns:
            Feedback or None: El objeto de feedback si existe, de lo contrario None.
        """
        try:
            return Feedback.query.get(feedback_id)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def get_feedbacks_by_evaluation(evaluation_id):
        """
        Obtiene todos los feedbacks relacionados con una evaluación específica.
        
        Parameters:
            evaluation_id (int): ID de la evaluación.
        
        Returns:
            List[Feedback]: Lista de objetos de feedback.
        """
        try:
            return Feedback.query.filter_by(id_evaluation=evaluation_id).all()
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def get_feedbacks_by_user(user_id):
        """
        Obtiene todos los feedbacks realizados por un usuario específico.
        
        Parameters:
            user_id (int): ID del usuario.
        
        Returns:
            List[Feedback]: Lista de objetos de feedback.
        """
        try:
            return Feedback.query.filter_by(id_user=user_id).all()
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def update_feedback(feedback_id, feedback_text=None):
        """
        Actualiza un registro de feedback existente.
        
        Parameters:
            feedback_id (int): ID del feedback a actualizar.
            feedback_text (str, optional): Nuevo texto de retroalimentación.
        
        Returns:
            Feedback or None: El objeto de feedback actualizado si se encontró, de lo contrario None.
        """
        try:
            feedback = Feedback.query.get(feedback_id)
            if feedback is None:
                return None

            if feedback_text:
                feedback.feedback_text = feedback_text

            db.session.commit()
            return feedback
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_feedback(feedback_id):
        """
        Elimina un registro de feedback por su ID.
        
        Parameters:
            feedback_id (int): ID del feedback a eliminar.
        
        Returns:
            Feedback or None: El objeto de feedback eliminado si se encontró, de lo contrario None.
        """
        try:
            feedback = Feedback.query.get(feedback_id)
            if feedback is None:
                return None

            db.session.delete(feedback)
            db.session.commit()
            return feedback
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_feedbacks_paginated(page, per_page, id_evaluation=None, id_user=None):
        """
        Obtiene una lista paginada de feedbacks, con filtros opcionales.
        
        Parameters:
            page (int): Número de página.
            per_page (int): Número de registros por página.
            id_evaluation (int, optional): Filtrar por ID de evaluación.
            id_user (int, optional): Filtrar por ID de usuario.
        
        Returns:
            Pagination: Objeto de paginación que contiene los feedbacks y la información de la página.
        """
        try:
            query = Feedback.query

            if id_evaluation:
                query = query.filter(Feedback.id_evaluation == id_evaluation)
            if id_user:
                query = query.filter(Feedback.id_user == id_user)

            return query.paginate(page=page, per_page=per_page, error_out=False)
        except SQLAlchemyError as e:
            raise e
