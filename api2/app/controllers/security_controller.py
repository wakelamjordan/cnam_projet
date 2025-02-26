from flask import Blueprint, request, jsonify, current_app
from app.services.user_service import find_by_email
from werkzeug.security import check_password_hash
from app.models.user_model import User
from app.errors.security_error import LoginError
from app.config import limiter
from flask_limiter.errors import RateLimitExceeded
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import timedelta
import jwt

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

            access_token = create_access_token(
                identity=user_find.get_email(),
                additional_claims={"firstname": user_find.get_firstname()},
                expires_delta=timedelta(hours=1))

            return jsonify({
                "message": "Login successful",
                "token": access_token
            }), 200

        except LoginError as e:
            return jsonify({"error": str(e)}), 401

    @security_blueprint.route('/secure/')
    @jwt_required()
    def secure():
        current_user = get_jwt_identity()
        payload = get_jwt()
        print(payload)
        return jsonify(logged_in_as=current_user), 200

    @security_blueprint.errorhandler(RateLimitExceeded)
    def handle_rate_limit_error(e):
        # Personnaliser le message d'erreur
        return jsonify({
            "error": "Too many requests",
            "message":
            str(e.description),  # Afficher la description de l'erreur
        }), 429
