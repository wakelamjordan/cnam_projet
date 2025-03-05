from flask import Blueprint, request, jsonify
from app.services.security_service import login as login_service, password_reset as reset_service, token_check, token_insert
from app.errors.security_error import LoginError, TokenAlreadyUsed
from app.config import limiter
from flask_limiter.errors import RateLimitExceeded
from flask_jwt_extended import create_access_token, decode_token
from datetime import timedelta, date
from app.validators.user_validator import User_validator
from app.errors.user_error import UserEmailNotValide
from app.services.user_service import update
from app.controllers.user_controller import generate_password_hash
from app.errors.user_error import UserNotFoundError, UserPasswordNotValid

security_blueprint = Blueprint('security', __name__)


class SecurityController:
    """
    Controller for managing user security operations.
    
    This controller handles user authentication, registration, token management, and password reset operations.
    """

    @staticmethod
    @security_blueprint.route('/login', methods=['POST'])
    @limiter.limit("5/minute")
    def login():
        """
        Authenticates a user and generates a JWT token.
        
        Extracts login information from the JSON request, validates the email and password,
        and generates a JWT token if successful.
        
        Returns:
            JSON: Response containing the JWT token or an error message.
        """
        try:
            data: dict = request.json
            if not data["email"] or not data["password"]:
                raise LoginError("Email and password are required.")
            User_validator.validate_email(data["email"])
            user = login_service(data)

            access_token = create_access_token(
                identity=user["email"],
                additional_claims={
                    "firstname": user["firstname"],
                    "role": user["role"]
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
        """
        Validates a registration token and generates a temporary token to complete the registration.
        
        Args:
            token (str): Confirmation token received via email.
        
        Returns:
            JSON: Success message with a new token, or an error message if the token is invalid.
        """
        try:
            token_check(token)
            payload: dict = decode_token(token)
            token_new = create_access_token(
                payload['sub'],
                additional_claims={"type": "inscription_complete"},
                expires_delta=timedelta(minutes=30))
            token_insert(token_new)
            return jsonify({
                "message": "Validation ok, you can complete your information.",
                "token": token_new
            }), 200
        except (UserEmailNotValide, TokenAlreadyUsed) as e:
            return jsonify({"error": str(e)}), 415

    @staticmethod
    @security_blueprint.route('/inscription_complete', methods=['PATCH'])
    @limiter.limit("5/minute")
    def inscription_complete_patch():
        try:
            data: dict = request.json
            token_check(data["token"])
            payload: dict = decode_token(data["token"])

            User_validator.validate_psw(data["password"])
            data["password"] = generate_password_hash(data["password"],
                                                      method="pbkdf2:sha256",
                                                      salt_length=16)
            date_iso = date.fromisoformat(data["birth_at"])
            data["birth_at"] = date_iso
            updated_user = update(data, payload['sub'])
            return jsonify({"email": updated_user["email"]}), 200
        except (UserEmailNotValide, TokenAlreadyUsed) as e:
            return jsonify({"error": str(e)}), 415
        except UserPasswordNotValid as e:
            return jsonify({"error": str(e)}), 415

    @staticmethod
    @security_blueprint.route('/reset_request/<string:email>', methods=["GET"])
    @limiter.limit("5/minute")
    def password_reset_request(email: str):
        """
        Generates a password reset request.
        
        Args:
            email (str): The user's email address.
        
        Returns:
            JSON: Message indicating whether an email has been sent.
        """
        try:
            reset_service({"email": email})
        except UserNotFoundError:
            pass  # We do not want to reveal whether the email exists or not
        return jsonify({
            "message":
            f"If account {email} exist, you will receive a reset email."
        }), 200

    @staticmethod
    @security_blueprint.route('/reset/<string:token>', methods=["GET"])
    @limiter.limit("5/minute")
    def password_reset(token: str):
        """
        Verifies a password reset token and generates a new temporary token.
        
        Args:
            token (str): Password reset token sent via email.
        
        Returns:
            JSON: New temporary token to change the password, or an error message if invalid.
        """
        try:
            token_check(token)
            payload: dict = decode_token(token)
            new_token = create_access_token(
                payload['sub'],
                additional_claims={"type": "password_new"},
                expires_delta=timedelta(minutes=30))
            token_insert(new_token)
            return jsonify({
                "message": "You can set a new password",
                "token": new_token
            }), 200
        except (UserEmailNotValide, TokenAlreadyUsed) as e:
            return jsonify({"error": str(e)}), 415

    @staticmethod
    @security_blueprint.route('/password_new', methods=["PATCH"])
    @limiter.limit("5/minute")
    def password_new():
        """
        Changes the user's password after token verification.
        
        Returns:
            JSON: Confirmation message or an error if the token is invalid.
        """
        try:
            data: dict = request.json
            token_check(data['token'])
            payload: dict = decode_token(data['token'])
            User_validator.validate_psw(data["password"])
            data["password"] = generate_password_hash(data["password"],
                                                      method="pbkdf2:sha256",
                                                      salt_length=16)
            updated_user = update(data, payload['sub'])
            return jsonify({"email": updated_user["email"]}), 200
        except (UserEmailNotValide, TokenAlreadyUsed) as e:
            return jsonify({"error": str(e)}), 415
        except UserPasswordNotValid as e:
            return jsonify({"error": str(e)}), 415

    @security_blueprint.errorhandler(RateLimitExceeded)
    def handle_rate_limit_error(e):
        """
        Handles rate limit exceeded errors.
        
        Args:
            e (RateLimitExceeded): Rate limit error.
        
        Returns:
            JSON: Error message and 429 status code.
        """
        return jsonify({
            "error": "Too many requests",
            "message": str(e.description)
        }), 429
