from app.controllers.user_controller import user_blueprint
from app.controllers.security_controller import security_blueprint


def register_blueprints(app):
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(security_blueprint)
