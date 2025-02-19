from .user_controller import user_blueprint


def register_blueprints(app):
    app.register_blueprint(user_blueprint, url_prefix='/user')
