import os

from flask import Flask

from config import INSTANCE_DIR, Config
from database import Base, engine
import models  # noqa: F401 — registra os modelos no metadata


def create_app():
    os.makedirs(INSTANCE_DIR, exist_ok=True)

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    Base.metadata.create_all(bind=engine)

    from app.routes import bp as api_bp, paginas as paginas_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(paginas_bp)

    return app
