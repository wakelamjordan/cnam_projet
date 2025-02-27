from flask import Blueprint, request, jsonify
from app.services.security_service import login as login_service
from app.models.user_model import User
from app.errors.security_error import LoginError
from app.config import limiter
from flask_limiter.errors import RateLimitExceeded
from flask_jwt_extended import create_access_token
from datetime import timedelta
from app.validators.user_validator import User_validator
from app.errors.user_error import UserEmailNotValide

security_blueprint = Blueprint('security', __name__)


class SecurityController:

    @staticmethod
    @security_blueprint.route('/login/', methods=['POST'])
    @limiter.limit("2/minute")
    def login():
        try:
            data: dict = request.json

            if not data["email"] or not data["password"]:
                raise LoginError("Email and password are required.")
            User_validator.validate_email(data["email"])
            test = login_service(data)

            access_token = create_access_token(
                identity=test["email"],
                additional_claims={
                    "firstname": test["firstname"],
                    "role": test["role"]
                },
                expires_delta=timedelta(hours=1))

            return jsonify({
                "message": "Login successful",
                "token": access_token
            }), 200
        except UserEmailNotValide as e:
            return jsonify({"error": str(e)}), 415
        except LoginError as e:
            return jsonify({"error": str(e)}), 401

    @security_blueprint.errorhandler(RateLimitExceeded)
    def handle_rate_limit_error(e):
        # Personnaliser le message d'erreur
        return jsonify({
            "error": "Too many requests",
            "message":
            str(e.description),  # Afficher la description de l'erreur
        }), 429
