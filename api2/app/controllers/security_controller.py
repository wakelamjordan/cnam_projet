from flask import Blueprint, request, jsonify
from app.services.security_service import login as login_service
from app.errors.security_error import LoginError
from app.config import limiter
from flask_limiter.errors import RateLimitExceeded
from flask_jwt_extended import create_access_token, decode_token
from datetime import timedelta
from app.validators.user_validator import User_validator
from app.errors.user_error import UserEmailNotValide
from app.services.user_service import update
from datetime import date
from app.controllers.user_controller import generate_password_hash

security_blueprint = Blueprint('security', __name__)


class SecurityController:
    """
    Contrôleur pour gérer les opérations de sécurité, notamment l'authentification des utilisateurs.

    Cette classe contient des méthodes pour gérer les requêtes liées à la sécurité,
    telles que la connexion des utilisateurs et la gestion des erreurs de limite de taux.
    """

    @staticmethod
    @security_blueprint.route('/login', methods=['POST'])
    @limiter.limit("5/minute")
    def login():
        """
        Gère la connexion des utilisateurs.

        Cette méthode traite les requêtes POST à l'endpoint `/login/` pour authentifier les utilisateurs.
        Elle valide les informations d'identification, génère un token JWT en cas de succès,
        et gère les erreurs de validation et de connexion.

        Returns:
            JSON response: Réponse JSON contenant un message de succès et le token JWT,
                           ou un message d'erreur en cas d'échec.
        """
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

    @staticmethod
    @security_blueprint.route('/inscription_complete/<string:token>',
                              methods=['GET'])
    @limiter.limit("5/minute")
    def inscription_complete(token: str):
        try:
            # data: dict = request.json

            # if not data["email"] or not data["password"]:
            #     raise LoginError("Email and password are required.")
            # User_validator.validate_email(data["email"])
            # test = login_service(data)
            payload: dict = decode_token(token)

            token_to_inscription_complete_post = create_access_token(
                payload['sub'],
                additional_claims={"type": "inscription_complete"},
                expires_delta=timedelta(minut=30))

            return jsonify({
                "message": "Validation ok, you can complete your information.",
                "token": token_to_inscription_complete_post
            }), 200
        except UserEmailNotValide as e:
            return jsonify({"error": str(e)}), 415

    @staticmethod
    @security_blueprint.route('/inscription_complete', methods=['PATCH'])
    @limiter.limit("5/minute")
    def inscription_complete_patch():
        try:
            data: dict = request.json

            # if not data["email"] or not data["password"]:
            #     raise LoginError("Email and password are required.")
            # User_validator.validate_email(data["email"])
            # test = login_service(data)
            payload: dict = decode_token(data['token'])

            date_iso = date.fromisoformat(data["birth_at"])
            data["birth_at"] = date_iso

            password = data["password"]
            User_validator.validate_psw(password)
            password_hash = generate_password_hash(password,
                                                   method="pbkdf2:sha256",
                                                   salt_length=16)

            data["password"] = password_hash

            return jsonify({"email": update(data, payload['sub'])}), 200
        except UserEmailNotValide as e:
            return jsonify({"error": str(e)}), 415

    @security_blueprint.errorhandler(RateLimitExceeded)
    def handle_rate_limit_error(e):
        """
        Gère les erreurs de limite de taux.

        Cette méthode est un gestionnaire d'erreurs pour les exceptions `RateLimitExceeded`.
        Elle retourne une réponse JSON avec un message d'erreur indiquant que le taux de requêtes a été dépassé.

        Args:
            e (RateLimitExceeded): L'exception de limite de taux.

        Returns:
            JSON response: Réponse JSON contenant un message d'erreur et une description de l'exception.
        """
        return jsonify({
            "error": "Too many requests",
            "message": str(e.description),
        }), 429
