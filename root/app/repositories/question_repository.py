from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.questions import Question

class QuestionRepository:

    @staticmethod
    def create_question(name, value, id_evaluation):
        """
        Crea una nueva pregunta y la guarda en la base de datos.
        """
        try:
            new_question = Question(name=name, value=value, id_evaluation=id_evaluation)
            db.session.add(new_question)
            db.session.commit()
            return new_question
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_question_by_id(question_id):
        """
        Busca una pregunta por su ID.
        """
        try:
            return Question.query.get(question_id)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def get_questions_paginated(page, per_page, name=None):
        """
        Devuelve una lista paginada de preguntas, con filtro opcional por nombre.
        """
        try:
            query = Question.query
            
            # Filtrar por nombre si está presente
            if name:
                query = query.filter(Question.name.ilike(f"%{name}%"))
            
            return query.paginate(page=page, per_page=per_page, error_out=False)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def update_question(question_id, name=None, value=None, id_evaluation=None):
        """
        Actualiza una pregunta existente por su ID.
        """
        try:
            question = Question.query.get(question_id)
            if question is None:
                return None

            # Actualizar los campos proporcionados
            if name:
                question.name = name
            if value:
                question.value = value
            if id_evaluation:
                question.id_evaluation = id_evaluation

            db.session.commit()
            return question
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_question(question_id):
        """
        Elimina una pregunta por su ID.
        """
        try:
            question = Question.query.get(question_id)
            if question is None:
                return None

            db.session.delete(question)
            db.session.commit()
            return question
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
