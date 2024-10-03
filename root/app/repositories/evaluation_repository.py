from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models.evaluation import Evaluation

class EvaluationRepository:

    @staticmethod
    def create_evaluation(id, name, description=None, created_at=None):
        try:
            new_evaluation = Evaluation(id=id, name=name, description=description, created_at=created_at)
            db.session.add(new_evaluation)
            db.session.commit()
            return new_evaluation
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_evaluation_by_id(evaluation_id):
        try:
            return Evaluation.query.get(evaluation_id)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def get_evaluations_paginated(page, per_page, name=None, description=None):
        try:
            query = Evaluation.query
            
            if name:
                query = query.filter(Evaluation.name.ilike(f"%{name}%"))
            if description:
                query = query.filter(Evaluation.description.ilike(f"%{description}%"))
            
            return query.paginate(page=page, per_page=per_page, error_out=False)
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def update_evaluation(evaluation_id, name=None, description=None):
        try:
            evaluation = Evaluation.query.get(evaluation_id)
            if evaluation is None:
                return None

            if name:
                evaluation.name = name
            if description:
                evaluation.description = description

            db.session.commit()
            return evaluation
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_evaluation(evaluation_id):
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
