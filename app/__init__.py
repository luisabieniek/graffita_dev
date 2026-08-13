from flask import Flask

from config import Config
from app.routes import bp as api_bp, paginas as paginas_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(api_bp)
    app.register_blueprint(paginas_bp)

    return app