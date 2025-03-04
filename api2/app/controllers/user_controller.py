from flask import Blueprint, jsonify, request, Response
from app.services.user_service import (delete as
                                       service_delete, find_by_email as
                                       service_find_by_email, find_all as
                                       service_find_all, update as
                                       service_update, replace as
                                       service_replace)
from app.services.security_service import insert as service_security_insert
import string
import secrets
from app.errors.user_error import UserNotFoundError, UserEmailDoesExist, UserEmailNotValide, UserPasswordNotValid, UserDataIncomplete
from app.errors.security_error import AccessDenied
from datetime import date
from app.validators.user_validator import User_validator
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt

user_blueprint = Blueprint('user', __name__)

class UserController:
    """
    Contrôleur pour gérer les opérations CRUD sur les utilisateurs.

    Cette classe contient des méthodes pour gérer les requêtes liées aux utilisateurs,
    telles que la récupération, la création, la mise à jour et la suppression des utilisateurs.
    """

    @staticmethod
    @user_blueprint.route('', methods=['GET'])
    @jwt_required()
    def _get_all() -> Response:
        """
        Récupère tous les utilisateurs.

        Cette méthode traite les requêtes GET à l'endpoint `/` pour récupérer tous les utilisateurs.
        Elle vérifie que l'utilisateur est un administrateur avant de retourner la liste des utilisateurs.

        Returns:
            JSON response: Réponse JSON contenant la liste des utilisateurs,
                           ou un message d'erreur en cas d'échec.
        """
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
        """
        Récupère un utilisateur par son email.

        Cette méthode traite les requêtes GET à l'endpoint `/<string:email>` pour récupérer un utilisateur
        par son adresse email. Elle vérifie que l'utilisateur est un administrateur et que l'email est valide.

        Args:
            email (str): L'adresse email de l'utilisateur à récupérer.

        Returns:
            JSON response: Réponse JSON contenant les informations de l'utilisateur,
                           ou un message d'erreur en cas d'échec.
        """
        try:
            UserController._is_admin()
            User_validator.validate_email(email)
            entity_find = service_find_by_email({"email": email})
            return jsonify(entity_find), 200
        except UserEmailNotValide as e:
            return jsonify({"error": str(e)}), 415
        except UserNotFoundError:
            return jsonify({"error": f"Email {email} not found"}), 404
        except AccessDenied as e:
            return jsonify({"error": str(e)}), 403

    @staticmethod
    @user_blueprint.route('/<string:email>', methods=['PUT'])
    @jwt_required()
    def _put(email) -> Response:
        """
        Met à jour un utilisateur par son email.

        Cette méthode traite les requêtes PUT à l'endpoint `/<string:email>` pour mettre à jour un utilisateur
        par son adresse email. Elle vérifie que l'utilisateur est un administrateur, que l'email est valide,
        et que toutes les données requises sont présentes.

        Args:
            email (str): L'adresse email de l'utilisateur à mettre à jour.

        Returns:
            JSON response: Réponse JSON contenant les informations mises à jour de l'utilisateur,
                           ou un message d'erreur en cas d'échec.
        """
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
        except UserEmailNotValide as e:
            return jsonify({"error": str(e)}), 415
        except UserPasswordNotValid as e:
            return jsonify({"error": str(e)}), 415
        except AccessDenied as e:
            return jsonify({"error": str(e)}), 403

    @staticmethod
    @user_blueprint.route('/<string:email>', methods=['PATCH'])
    @jwt_required()
    def _patch(email) -> Response:
        """
        Met à jour partiellement un utilisateur par son email.

        Cette méthode traite les requêtes PATCH à l'endpoint `/<string:email>` pour mettre à jour partiellement
        un utilisateur par son adresse email. Elle vérifie que l'utilisateur est un administrateur et que l'email
        est valide.

        Args:
            email (str): L'adresse email de l'utilisateur à mettre à jour.

        Returns:
            JSON response: Réponse JSON contenant les informations mises à jour de l'utilisateur,
                           ou un message d'erreur en cas d'échec.
        """
        try:
            UserController._is_admin()
            data: dict = request.get_json()
            User_validator.validate_email(email)
            if "birth_at" in data:
                date_iso = date.fromisoformat(data["birth_at"])
                data["birth_at"] = date_iso
            if "password" in data:
                password = data["password"]
                User_validator.validate_psw(password)
                password_hash = generate_password_hash(password,
                                                       method="pbkdf2:sha256",
                                                       salt_length=16)
                data["password"] = password_hash
            entity_new = service_update(data, email)
            del entity_new["birth_at"], entity_new["created_at"], entity_new["login_at"]
            return jsonify(entity_new), 200
        except UserNotFoundError:
            return jsonify({"error": f"Email {email} not found"}), 404
        except UserPasswordNotValid as e:
            return jsonify({"error": str(e)}), 415
        except AccessDenied as e:
            return jsonify({"error": str(e)}), 403
        except UserEmailNotValide as e:
            return jsonify({"error": str(e)}), 415

    @classmethod
    @user_blueprint.route('/new', methods=['POST'])
    @jwt_required()
    def _new() -> Response:
        """
        Crée un nouvel utilisateur.

        Cette méthode traite les requêtes POST à l'endpoint `/new` pour créer un nouvel utilisateur.
        Elle vérifie que l'utilisateur est un administrateur et que l'email est valide.

        Returns:
            JSON response: Réponse JSON contenant l'email de l'utilisateur créé,
                           ou un message d'erreur en cas d'échec.
        """
        try:
            UserController._is_admin()
            data: dict = request.json
            User_validator.validate_email(data["email"])
            data["password"] = UserController._generate_psw()
            email_insert = service_security_insert(data)
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
        """
        Supprime un utilisateur.

        Cette méthode traite les requêtes DELETE à l'endpoint `/delete` pour supprimer un utilisateur.
        Elle vérifie que l'utilisateur est un administrateur et que l'email est valide.

        Returns:
            JSON response: Réponse JSON contenant un message de succès,
                           ou un message d'erreur en cas d'échec.
        """
        try:
            UserController._is_admin()
            data = request.json
            if "email" not in data:
                raise UserDataIncomplete()
            User_validator.validate_email(data["email"])
            service_delete(data)
            return jsonify({'message': 'User deleted successfully'}), 200
        except UserEmailNotValide as e:
            return jsonify({"error": str(e)}), 415
        except UserDataIncomplete as e:
            return jsonify({"error": str(e)}), 404
        except AccessDenied as e:
            return jsonify({"error": str(e)}), 403
        except UserNotFoundError:
            return jsonify({"error": f"Email {data["email"]} not found"}), 404

    @staticmethod
    def _generate_psw() -> str:
        """
        Génère un mot de passe aléatoire sécurisé.

        Cette méthode génère un mot de passe aléatoire sécurisé composé de lettres, chiffres et caractères spéciaux.

        Returns:
            str: Le mot de passe généré.
        """
        character_all = string.ascii_letters + string.digits + string.punctuation
        password: str = ''.join(
            secrets.choice(character_all) for _ in range(20))
        password = (secrets.choice(string.digits) for _ in range(1))
        password = f"{password}{(secrets.choice(string.punctuation) for _ in range(1))}"
        return password

    @staticmethod
    def _is_admin() -> bool:
        """
        Vérifie si l'utilisateur est un administrateur.

        Cette méthode vérifie si l'utilisateur actuellement authentifié a le rôle d'administrateur.
        Si ce n'est pas le cas, elle lève une exception `AccessDenied`.

        Returns:
            bool: True si l'utilisateur est un administrateur.

        Raises:
            AccessDenied: Si l'utilisateur n'est pas un administrateur.
        """
        payload = get_jwt()
        if payload.get("role") != "ROLE_ADMIN":
            raise AccessDenied()
        return True
