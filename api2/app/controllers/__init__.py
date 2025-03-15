from app.controllers.user_controller import user_blueprint
from app.controllers.security_controller import security_blueprint
from app.controllers.publication_controller import publication_blueprint
from app.controllers.category_controller import category_blueprint
from app.controllers.role_controller import role_blueprint
from app.controllers.home_page_content_controller import home_page_content_blueprint
from app.controllers.photo_controller import photo_blueprint


def register_blueprints(app):
    """
    Enregistre les blueprints de l'application Flask.

    Cette fonction enregistre les blueprints `user_blueprint` et `security_blueprint`
    dans l'application Flask, en spécifiant un préfixe d'URL pour `user_blueprint`.

    - `user_blueprint` est enregistré avec le préfixe d'URL `/user`.
    - `security_blueprint` est enregistré sans préfixe d'URL.

    Args:
        app (Flask): L'instance de l'application Flask dans laquelle les blueprints doivent être enregistrés.
    """
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(security_blueprint)
    app.register_blueprint(publication_blueprint)
    app.register_blueprint(category_blueprint, url_prefix='/category')
    app.register_blueprint(role_blueprint, url_prefix='/role')
    app.register_blueprint(home_page_content_blueprint,
                           url_prefix='/home_page_content')
    app.register_blueprint(photo_blueprint, url_prefix='/photo')
