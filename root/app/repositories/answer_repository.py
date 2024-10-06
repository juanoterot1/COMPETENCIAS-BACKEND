from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.answer import Answer

class AnswerRepository:

    @staticmethod
    def create_answer(answer_description, id_evaluation, id_question, id_user, score=None):
        """
        Crea una nueva respuesta y la guarda en la base de datos.
        """
        try:
            new_answer = Answer(
                answer_description=answer_description,
                id_evaluation=id_evaluation,
                id_question=id_question,
                id_user=id_user,
                score=score
            )
            db.session.add(new_answer)
            db.session.commit()
            return new_answer
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_answer_by_id(answer_id):
        """
        Busca una respuesta por su ID.
        """
        try:
            return Answer.query.get(answer_id)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def get_answers_paginated(page, per_page, id_evaluation=None):
        """
        Devuelve una lista paginada de respuestas, con un filtro opcional por evaluación.
        """
        try:
            query = Answer.query
            
            # Filtrar por evaluación si está presente
            if id_evaluation:
                query = query.filter(Answer.id_evaluation == id_evaluation)
            
            return query.paginate(page=page, per_page=per_page, error_out=False)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def update_answer(answer_id, answer_description=None, score=None):
        """
        Actualiza una respuesta existente por su ID.
        """
        try:
            answer = Answer.query.get(answer_id)
            if answer is None:
                return None

            # Actualizar los campos proporcionados
            if answer_description:
                answer.answer_description = answer_description
            if score is not None:
                answer.score = score

            db.session.commit()
            return answer
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_answer(answer_id):
        """
        Elimina una respuesta por su ID.
        """
        try:
            answer = Answer.query.get(answer_id)
            if answer is None:
                return None

            db.session.delete(answer)
            db.session.commit()
            return answer
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
