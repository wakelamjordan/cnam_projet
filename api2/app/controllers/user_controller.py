from flask import Blueprint, jsonify, request, Response
from app.models.user_model import User as Entity
from app.services.user_service import (insert as service_insert, delete as
                                       service_delete, find_by_email as
                                       service_find_by_email, find_all as
                                       service_find_all, update as
                                       service_update, replace as
                                       service_replace)
import string
import secrets
from app.errors.user_error import UserNotFoundError, UserEmailDoesExist, UserEmailNotValide, UserPasswordNotValid, UserDataIncomplete
from app.errors.security_error import AccessDenied
from datetime import date
from app.validators.user_validator import User_validator
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt
from werkzeug.exceptions import Forbidden

# Création d'un Blueprint Flask pour regrouper les routes liées aux utilisateurs
user_blueprint = Blueprint('user', __name__)


class UserController:

    @staticmethod
    @user_blueprint.route('/', methods=['GET'])
    @jwt_required()
    def _get_all() -> Response:
        try:
            UserController._is_admin()
            result: list = service_find_all()
            return jsonify(result), 200
        except AccessDenied as e:
            return jsonify({"error": str(e)}), 403

    @staticmethod
    @user_blueprint.route('/<string:email>', methods=['GET'])
    @jwt_required()
    def _get_one(email) -> Response:
        try:
            UserController._is_admin()
            User_validator.validate_email(email)
            entity_find = service_find_by_email({"email": email})
            return jsonify(entity_find), 200
        except UserEmailNotValide as e:
            return jsonify({"error": str(e)}), 415
        except UserNotFoundError as e:
            return jsonify({"error": str(e)}), 404
        except AccessDenied as e:
            return jsonify({"error": str(e)}), 403

    @staticmethod
    @user_blueprint.route('/<string:email>', methods=['PUT'])
    @jwt_required()
    def _put(email) -> Response:
        try:
            UserController._is_admin()
            data: dict = request.get_json()
            User_validator.validate_email(email)

            if "email" not in data or "role" not in data or "firstname" not in data or "lastname" not in data or "password" not in data or "birth_at" not in data:
                raise UserDataIncomplete
            date_iso = date.fromisoformat(data["birth_at"])
            data["birth_at"] = date_iso

            password = data["password"]
            User_validator.validate_psw(password)
            password_hash = generate_password_hash(password,
                                                   method="pbkdf2:sha256",
                                                   salt_length=16)
            data["password"] = password_hash
            entity_new = service_replace(data, email)
            return jsonify(entity_new), 200

        except UserDataIncomplete as e:
            return jsonify({"error": str(e)}), 400
        except UserNotFoundError:
            return jsonify({"error": f"Email {email} not found"}), 404
        except UserPasswordNotValid as e:
            return jsonify({"error": str(e)}), 415
        except AccessDenied as e:
            return jsonify({"error": str(e)}), 403

    @staticmethod
    @user_blueprint.route('/<string:email>', methods=['PATCH'])
    @jwt_required()
    def _patch(email) -> Response:
        try:
            UserController._is_admin()
            data: dict = request.get_json()
            User_validator.validate_email(email)
            if "birth_at" in data:
                date_iso = date.fromisoformat(data["birth_at"])
                # entity.set_birth_at()
                data["birth_at"] = date_iso
            if "password" in data:
                password = data["password"]
                User_validator.validate_psw(password)
                password_hash = generate_password_hash(password,
                                                       method="pbkdf2:sha256",
                                                       salt_length=16)
                data["password"] = password_hash
            entity_new = service_update(data, email)
            return jsonify(entity_new), 200
        except UserNotFoundError:
            return jsonify({"error": f"Email {email} not found"}), 404
        except UserPasswordNotValid as e:
            return jsonify({"error": str(e)}), 415
        except AccessDenied as e:
            return jsonify({"error": str(e)}), 403
 
    @classmethod
    @user_blueprint.route('/new', methods=['POST'])
    @jwt_required()
    def _new() -> Response:
        try:
            UserController._is_admin()
            data: dict = request.json
            User_validator.validate_email(data["email"])
            # entity = Entity(email)

            data["password"] = UserController._generate_psw()
            email_insert = service_insert(data)
            return jsonify({'email': email_insert}), 201
        except UserEmailNotValide as e:
            return jsonify({"error": str(e)}), 415
        except UserEmailDoesExist:
            return jsonify({"error": f"Email {data["email"]} does exist"}), 400
        except AccessDenied as e:
            return jsonify({"error": str(e)}), 403

    @staticmethod
    @user_blueprint.route('/delete', methods=['DELETE'])
    @jwt_required()
    def _delete() -> Response:
        try:
            UserController._is_admin()
            data = request.json
            if "email" not in data :
                raise UserDataIncomplete()
            User_validator.validate_email(data["email"])
            # entity = Entity(data["email"])
            service_delete(data)  # Suppression de l'utilisateur
            return jsonify({'message': 'User deleted successfully'}), 200
        except UserEmailNotValide as e:
            return jsonify({"error": str(e)}), 415
        except UserDataIncomplete as e:
            return jsonify({"error": str(e)}), 404
        except AccessDenied as e:
            return jsonify({"error": str(e)}), 403
        except UserNotFoundError as e:
            return jsonify({"error": str(e)}), 404

    def _generate_psw() -> str:
        # Génération d'un mot de passe aléatoire sécurisé
        character_all = string.ascii_letters + string.digits + string.punctuation
        password: str = ''.join(
            secrets.choice(character_all) for _ in range(20))
        password = (secrets.choice(string.digits) for _ in range(1))
        password = f"{password}{(secrets.choice(string.punctuation) for _ in range(1))}"
        return password

    def _is_admin() -> bool:
        payload = get_jwt()
        if payload.get("role") != "ROLE_ADMIN":
            raise AccessDenied()
        return True
