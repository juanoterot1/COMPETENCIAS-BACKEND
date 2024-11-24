from flask import Flask
from flask_cors import CORS
from flask_injector import FlaskInjector
from injector import singleton
from app.extensions import db
from app.extensions import init_logging


from app.controllers.tenants_controller import tenant_bp
from app.controllers.evaluation_controller import evaluation_bp
from app.controllers.user_controller import user_bp
from app.controllers.faculty_controller import faculty_bp 
from app.controllers.subject_controller import subject_bp
from app.controllers.question_controller import question_bp
from app.controllers.answer_controller import answer_bp
from app.controllers.grading_matrix_controller import grading_matrix_bp
from app.controllers.role_controller import role_bp 
from app.controllers.permission_controller import permission_bp
from app.controllers.feedback_controller import feedback_bp


from app.services.tenants_service import TenantService
from app.services.evaluation_service import EvaluationService
from app.services.user_service import UserService
from app.services.faculty_service import FacultyService 
from app.services.subject_service import SubjectService 
from app.services.question_service import QuestionService
from app.services.answer_service import AnswerService
from app.services.grading_matrix_service import GradingMatrixService
from app.services.role_service import RoleService
from app.services.permission_service import PermissionService
from app.services.feedback_service import FeedbackService


def configure(binder):
    binder.bind(TenantService, to=TenantService, scope=singleton)
    binder.bind(EvaluationService, to=EvaluationService, scope=singleton)
    binder.bind(UserService, to=UserService, scope=singleton)
    binder.bind(FacultyService, to=FacultyService, scope=singleton)
    binder.bind(SubjectService, to=SubjectService, scope=singleton)
    binder.bind(QuestionService, to=QuestionService, scope=singleton)
    binder.bind(AnswerService, to=AnswerService, scope=singleton)
    binder.bind(GradingMatrixService, to=GradingMatrixService, scope=singleton)
    binder.bind(RoleService, to=RoleService, scope=singleton)
    binder.bind(PermissionService, to=PermissionService, scope=singleton)
    binder.bind(FeedbackService, to=FeedbackService, scope=singleton)


def create_app():
    app = Flask(__name__)

    @app.teardown_request
    def teardown_request(exception=None):
        db.session.remove()

    CORS(app)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    logger = init_logging()
    logger.info(f"API MOBILE INVOKE")

    app.register_blueprint(tenant_bp, url_prefix='/api/v1')
    app.register_blueprint(evaluation_bp, url_prefix='/api/v1')
    app.register_blueprint(user_bp, url_prefix='/api/v1')
    app.register_blueprint(faculty_bp, url_prefix='/api/v1')
    app.register_blueprint(subject_bp, url_prefix='/api/v1')
    app.register_blueprint(question_bp, url_prefix='/api/v1')
    app.register_blueprint(answer_bp, url_prefix='/api/v1')
    app.register_blueprint(grading_matrix_bp, url_prefix='/api/v1')
    app.register_blueprint(role_bp, url_prefix='/api/v1')
    app.register_blueprint(permission_bp, url_prefix='/api/v1')
    app.register_blueprint(feedback_bp, url_prefix='/api/v1')



    FlaskInjector(app=app, modules=[configure])

    return app
