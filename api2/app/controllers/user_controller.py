from flask import Blueprint, jsonify, request, Response
from app.models.user_model import User as Entity
from app.services.user_service import insert as service_insert, delete as service_delete, find_by_email as service_find_by_email, find_all as service_find_all, update as service_update
import string, secrets
from app.errors.user_error import UserNotFoundError, UserEmailDoesExist, UserEmailNotValide
from datetime import date
from app.validators.user_validator import User_validator

# Création d'un Blueprint Flask pour regrouper les routes liées aux utilisateurs
user_blueprint = Blueprint('user', __name__)


class UserController:
    """
    Contrôleur pour la gestion des utilisateurs.

    Cette classe définit les routes permettant d'interagir avec les utilisateurs,
    notamment pour la récupération, la création, la mise à jour et la suppression d'utilisateurs.

    Les méthodes sont définies comme statiques, car elles sont directement associées
    aux routes de l'API et ne nécessitent pas d'instance de la classe.
    """

    @staticmethod
    @user_blueprint.route('/', methods=['GET', 'PUT', 'PATCH'])
    def _index():
        """
        Gère la récupération et la mise à jour des utilisateurs.

        - GET : Retourne tous les utilisateurs ou un utilisateur spécifique si un email est fourni.
        - PUT/PATCH : Met à jour les informations d'un utilisateur en fonction de son email.

        Retourne :
            - 200 OK : Si l'opération est réussie.
            - 404 Not Found : Si l'utilisateur recherché n'est pas trouvé.
        """
        method: str = request.method
        data: dict = request.get_json(silent=True)
        email: str = None
        if data != None:
            email = data['email']
        # print(request.args.get("email"))

        # print(data)
        # return jsonify({"jhjhj": "uyuyy"}), 200

        def _update() -> Response:
            """
            Met à jour les informations d'un utilisateur existant.

            - Récupère les données à modifier depuis `request.form`.
            - Met à jour uniquement les champs fournis.
            """
            entity = Entity(email)

            if data["firstname"]:
                entity.set_firstname(data["firstname"])
            if data["lastname"]:
                entity.set_lastname(data["lastname"])
            if data["birth_at"]:
                date_iso = date.fromisoformat(data["birth_at"])
                entity.set_birth_at(date_iso)

            entity_find = service_update(entity)
            return jsonify(entity_find.to_dict()), 200

        def _get_one():
            """
            Récupère un utilisateur en fonction de son email.
            """
            try:
                # data = request.json
                entity: Entity = Entity(request.args.get("email"))
                entity_find = service_find_by_email(entity)
                return jsonify(entity_find.to_dict()), 200
            except UserNotFoundError as e:
                return jsonify({"error": str(e)}), 404

        def _get_all():
            """
            Récupère la liste de tous les utilisateurs.
            """
            result: list = [
                element.to_dict() for element in service_find_all()
            ]
            return jsonify(result), 200

        if method in ['PUT', 'PATCH']:
            return _update()
        # elif method == 'GET' and email != None:
        elif method == 'GET' and request.args.get("email"):
            return _get_one()
        else:
            return _get_all()

    @staticmethod
    @user_blueprint.route('/new', methods=['POST'])
    def _new() -> Response:
        """
        Crée un nouvel utilisateur avec une adresse email et un mot de passe aléatoire.

        - L'email est récupéré depuis `request.form`.
        - Un mot de passe aléatoire de 20 caractères est généré.
        - L'utilisateur est inséré dans la base de données.

        Retourne :
            - 201 Created : Si l'utilisateur est bien créé.
            - 404 Not Found : Si l'email est déjà utilisé (exception `UserEmailDoesExist`).
        """
        try:
            # email = request.form.get('email')
            # data = Entity(email)  # Création d'une instance User
            data: dict = request.json

            email: str = data['email']

            validator: User_validator = User_validator

            print(validator.validate_email(validator, email))

            entity = Entity(email)

            # Génération d'un mot de passe aléatoire sécurisé
            character_all = string.ascii_letters + string.digits
            password: str = ''.join(
                secrets.choice(character_all) for _ in range(20))

            entity.set_password(password)  # Définition du mot de passe
            email_insert = service_insert(
                entity)  # Insertion en base de données

        # except UserEmailDoesExist as e:
        #     return jsonify({"error": str(e)}), 404
        except UserEmailNotValide as e:
            return jsonify({"error": str(e)}), 404

        return jsonify({'email': email_insert}), 201

    @staticmethod
    @user_blueprint.route('/delete', methods=['DELETE'])
    def _delete() -> Response:
        """
        Supprime un utilisateur de la base de données en fonction de son email.

        - L'email est récupéré depuis `request.form`.
        - Si l'utilisateur existe, il est supprimé.
        - Sinon, une erreur est retournée.

        Retourne :
            - 200 OK : Si l'utilisateur est bien supprimé.
            - 404 Not Found : Si aucun utilisateur correspondant n'est trouvé.
        """
        try:
            data = request.json
            entity = Entity(data["email"])  # Création d'une instance User
            service_delete(entity)  # Suppression de l'utilisateur
            return jsonify({'message': 'User deleted successfully'}), 200

        except UserNotFoundError as e:
            return jsonify({"error": str(e)}), 404
