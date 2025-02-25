from flask import Blueprint, jsonify, request, Response
from app.models.user_model import User as Entity
from app.services.user_service import (insert as service_insert, delete as
                                       service_delete, find_by_email as
                                       service_find_by_email, find_all as
                                       service_find_all, update as
                                       service_update)
import string
import secrets
from app.errors.user_error import UserNotFoundError, UserEmailDoesExist, UserEmailNotValide, UserPasswordNotValid
from datetime import date
from app.validators.user_validator import User_validator
from werkzeug.security import generate_password_hash

# Création d'un Blueprint Flask pour regrouper les routes liées aux utilisateurs
user_blueprint = Blueprint('user', __name__)


class UserController:
    """
    Contrôleur pour la gestion des utilisateurs.

    Cette classe définit les routes permettant d'interagir avec les utilisateurs,
    notamment pour la récupération, la création, la mise à jour et la suppression d'utilisateurs.

    Toutes les méthodes sont statiques car elles sont directement associées aux routes de l'API.
    """

    @staticmethod
    @user_blueprint.route('/', methods=['GET', 'PUT', 'PATCH'])
    def _index() -> Response:
        """
        Gère la récupération et la mise à jour des utilisateurs.

        - **GET** : Retourne tous les utilisateurs ou un utilisateur spécifique si un email est fourni en paramètre.
        - **PUT/PATCH** : Met à jour les informations d'un utilisateur en fonction de son email.

        Retourne :
            - **200 OK** : Si l'opération est réussie.
            - **404 Not Found** : Si l'utilisateur recherché n'est pas trouvé.
        """
        method: str = request.method
        data: dict = request.get_json(silent=True)
        email: str = data.get('email') if data else None

        def _update() -> Response:
            """
            Met à jour les informations d'un utilisateur existant.

            - Récupère les données à modifier depuis `request.form`.
            - Met à jour uniquement les champs fournis.

            Retourne :
                - **200 OK** : Si l'utilisateur est mis à jour avec succès.
                - **404 Not Found** : Si l'utilisateur n'est pas trouvé.
            """
            try:
                User_validator.validate_email(email)
                entity = Entity(email)

                if "firstname" in data:
                    entity.set_firstname(data["firstname"])
                if "lastname" in data:
                    entity.set_lastname(data["lastname"])
                if "birth_at" in data:
                    date_iso = date.fromisoformat(data["birth_at"])
                    entity.set_birth_at(date_iso)
                if "password" in data:
                    password = data["password"]
                    User_validator.validate_psw(password)
                    password_hash = generate_password_hash(
                        password, method="pbkdf2:sha256", salt_length=16)
                    entity.set_password(password_hash)

                entity_find = service_update(entity)
                return jsonify(entity_find.to_dict()), 200

            except UserNotFoundError:
                return jsonify({"error": f"Email {email} not found"}), 404
            except UserPasswordNotValid as e:
                return jsonify({"error": str(e)}), 415

        def _get_one() -> Response:
            """
            Récupère un utilisateur en fonction de son email.

            Retourne :
                - **200 OK** : Si l'utilisateur est trouvé.
                - **404 Not Found** : Si l'utilisateur n'est pas trouvé.
            """
            try:
                User_validator.validate_email(request.args.get("email"))
                entity = Entity(request.args.get("email"))
                entity_find = service_find_by_email(entity)
                return jsonify(entity_find.to_dict()), 200
            except UserEmailNotValide as e:
                return jsonify({"error": str(e)}), 415
            except UserNotFoundError as e:
                return jsonify({"error": str(e)}), 404

        def _get_all() -> Response:
            """
            Récupère la liste de tous les utilisateurs.

            Retourne :
                - **200 OK** : Liste de tous les utilisateurs.
            """
            result: list = [
                element.to_dict() for element in service_find_all()
            ]
            return jsonify(result), 200

        if method in ['PUT', 'PATCH']:
            return _update()
        elif method == 'GET' and request.args.get("email"):
            return _get_one()
        else:
            return _get_all()

    @classmethod
    @user_blueprint.route('/new', methods=['POST'])
    def _new() -> Response:
        """
        Crée un nouvel utilisateur avec une adresse email et un mot de passe aléatoire.

        - L'email est récupéré depuis `request.json`.
        - Un mot de passe aléatoire de 20 caractères est généré.
        - L'utilisateur est inséré dans la base de données.

        Retourne :
            - **201 Created** : Si l'utilisateur est bien créé.
            - **400 Bad Request** : Si l'email est déjà utilisé (`UserEmailDoesExist`).
            - **415 Unsupported Media Type** : Si l'email n'est pas valide (`UserEmailNotValide`).
        """
        try:
            data: dict = request.json
            email: str = data['email']
            User_validator.validate_email(email)
            entity = Entity(email)

            entity.set_password(
                UserController._generate_psw())  # Définition du mot de passe
            email_insert = service_insert(
                entity)  # Insertion en base de données
        except UserEmailNotValide as e:
            return jsonify({"error": str(e)}), 415
        except UserEmailDoesExist:
            return jsonify({"error": f"Email {email} does exist"}), 400

        return jsonify({'email': email_insert}), 201

    @staticmethod
    @user_blueprint.route('/delete', methods=['DELETE'])
    def _delete() -> Response:
        """
        Supprime un utilisateur de la base de données en fonction de son email.

        - L'email est récupéré depuis `request.json`.
        - Si l'utilisateur existe, il est supprimé.
        - Sinon, une erreur est retournée.

        Retourne :
            - **200 OK** : Si l'utilisateur est bien supprimé.
            - **404 Not Found** : Si aucun utilisateur correspondant n'est trouvé.
        """
        try:
            data = request.json
            User_validator.validate_email(data["email"])
            entity = Entity(data["email"])
            service_delete(entity)  # Suppression de l'utilisateur
            return jsonify({'message': 'User deleted successfully'}), 200
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
