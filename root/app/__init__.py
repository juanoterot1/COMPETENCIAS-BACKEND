from flask import Flask
from flask_cors import CORS
from flask_injector import FlaskInjector
from injector import singleton
from app.extensions import db
from app.extensions import init_logging

# Import Controllers
from app.controllers.tenants_controller import tenant_bp
from app.controllers.evaluation_controller import evaluation_bp
from app.controllers.user_controller import user_bp

# Import Services
from app.services.tenants_service import TenantService
from app.services.evaluation_service import EvaluationService
from app.services.user_service import UserService

def configure(binder):
    binder.bind(TenantService, to=TenantService, scope=singleton)
    binder.bind(EvaluationService, to=EvaluationService, scope=singleton)
    binder.bind(UserService, to=UserService, scope=singleton)

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

    # Register blueprints
    app.register_blueprint(tenant_bp, url_prefix='/api/v1')
    app.register_blueprint(evaluation_bp, url_prefix='/api/v1')
    app.register_blueprint(user_bp, url_prefix='/api/v1')

    FlaskInjector(app=app, modules=[configure])

    return app
