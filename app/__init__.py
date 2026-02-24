from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    print("DATABASE_URL =", os.getenv("DATABASE_URL"))
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # register models
    from app.models import User, Task

    return app
