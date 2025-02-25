from flask import Flask
from app.controllers import register_blueprints
from app.models import init_db
from app.config import Config, Test_config
import os


def create_app():
    app = Flask(__name__)

    if os.getenv("FLASK_ENV") == "testing":
        app.config.from_object(Test_config)
    else:
        app.config.from_object(Config)
    with app.app_context():
        init_db()
    register_blueprints(app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
