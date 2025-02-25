from flask import Blueprint, request, jsonify
from app.services.user_service import find_by_email
from werkzeug.security import check_password_hash
from app.models.user_model import User
from app.errors.security_error import LoginError
from app.config import limiter
from flask_limiter.errors import RateLimitExceeded
from flask_jwt import JWT, jwt_required, current_identity

security_blueprint = Blueprint('security', __name__)


class SecurityController:

    @staticmethod
    @security_blueprint.route('/login/', methods=['POST'])
    @limiter.limit("2/minute")
    def login():
        try:
            # Récupération des données JSON envoyées
            data = request.json
            email = data.get("email")
            password = data.get("password")

            if not email or not password:
                raise LoginError("Email and password are required.")

            # Recherche de l'utilisateur
            user_find = find_by_email(User(email))

            if not user_find:
                raise LoginError("Invalid email or password.")

            # Vérification du mot de passe hashé
            if not check_password_hash(user_find.get_password(), password):
                raise LoginError("Invalid email or password.")

            jwt = JWT(user_find.get_email(), identity)
            return jsonify({
                "message": "Login successful",
                "token": "your_jwt_token"
            }), 200

        except LoginError as e:
            return jsonify({"error": str(e)}), 401

    @security_blueprint.route('/secure/')
    @jwt_required()
    def secure():
        return jsonify({"message": "route sécurisée"}), 200

    @security_blueprint.errorhandler(RateLimitExceeded)
    def handle_rate_limit_error(e):
        # Personnaliser le message d'erreur
        return jsonify({
            "error": "Too many requests",
            "message":
            str(e.description),  # Afficher la description de l'erreur
        }), 429
