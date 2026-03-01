from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # register models
    from app.models import User, Task
    from app.auth.routes import auth_bp
    from app.tasks import tasks_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp, url_prefix="/tasks")

    return app
