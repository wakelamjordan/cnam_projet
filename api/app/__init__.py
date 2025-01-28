from flask import Flask
from app.manager.database import db_session
from app.config import config
import os

app = Flask(__name__)

# Ensure correct configuration class is used
app.config.from_object(config[os.getenv(
    'FLASK_ENV', 'dev')])  # Change 'DevelopmentConfig' as needed

from app.routes import *


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()  # Close database session after each request


if __name__ == "__main__":
    app.run(debug=True)
