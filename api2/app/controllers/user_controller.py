from flask import Blueprint, jsonify, request
from ..models.user_model import User as Entity
from ..services.user_service import insert, delete, find_by_email, find_all
import string, secrets
from ..errors.user_error import UserNotFoundError, UserEmailDoesExist

# Création d'un Blueprint Flask pour regrouper les routes liées aux utilisateurs
user_blueprint = Blueprint('user', __name__)


class UserController:
    """
    Contrôleur pour la gestion des utilisateurs.

    Cette classe définit les routes permettant d'interagir avec les utilisateurs,
    notamment pour la récupération, l'ajout et la suppression d'utilisateurs.

    Les méthodes sont définies comme statiques, car elles sont directement associées
    aux routes de l'API et ne nécessitent pas d'instance de la classe.
    """

    @staticmethod
    @user_blueprint.route('/', methods=['GET'])
    def index():
        """
        Récupère la liste des utilisateurs ou un utilisateur spécifique via son email.

        - Si un paramètre `email` est fourni dans la requête, il retourne l'utilisateur correspondant.
        - Sinon, il retourne la liste complète des utilisateurs.

        Retourne :
            - 200 OK : Si un ou plusieurs utilisateurs sont trouvés.
            - 404 Not Found : Si aucun utilisateur correspondant n'est trouvé.

        Exemple d'utilisation :
            - GET /user/?email=exemple@email.com -> Retourne l'utilisateur avec cet email.
            - GET /user/ -> Retourne tous les utilisateurs.
        """
        email = request.args.get('email')

        if email:
            try:
                entity = Entity(email)  # Création d'une instance User
                entity_find = find_by_email(
                    entity)  # Recherche dans la base de données
                print(entity_find)
                return jsonify(entity_find.to_dict()), 200
            except UserNotFoundError as e:
                return jsonify({"error": str(e)}), 404
        else:
            result = [element.to_dict() for element in find_all()
                      ]  # Récupération de tous les utilisateurs
            return jsonify(result), 200

    @staticmethod
    @user_blueprint.route('/new', methods=['POST'])
    def new():
        """
        Crée un nouvel utilisateur avec une adresse email et un mot de passe aléatoire.

        - L'email est récupéré depuis `request.form`.
        - Un mot de passe aléatoire de 20 caractères est généré.
        - L'utilisateur est inséré dans la base de données.

        Retourne :
            - 200 OK : Si l'utilisateur est bien créé.
            - 404 Not Found : Si l'email est déjà utilisé (exception `UserEmailDoesExist`).

        Exemple d'utilisation :
            - POST /user/new (avec un `form-data` contenant `email`).
        """
        try:
            email = request.form.get('email')
            data = Entity(email)  # Création d'une instance User

            # Génération d'un mot de passe aléatoire sécurisé
            character_all = string.ascii_letters + string.digits
            password: str = ''.join(
                secrets.choice(character_all) for _ in range(20))

            data.set_password(password)  # Définition du mot de passe
            insert(data)  # Insertion en base de données

        except UserEmailDoesExist as e:
            return jsonify({"error": str(e)}), 404

        return jsonify({'email': email}), 200

    @staticmethod
    @user_blueprint.route('/delete', methods=['DELETE'])
    def delete():
        """
        Supprime un utilisateur de la base de données en fonction de son email.

        - L'email est récupéré depuis `request.form`.
        - Si l'utilisateur existe, il est supprimé.
        - Sinon, une erreur est retournée.

        Retourne :
            - 200 OK : Si l'utilisateur est bien supprimé.
            - 404 Not Found : Si aucun utilisateur correspondant n'est trouvé.

        Exemple d'utilisation :
            - DELETE /user/delete (avec un `form-data` contenant `email`).
        """
        try:
            email = request.form.get('email')
            entity = Entity(email)  # Création d'une instance User
            delete(entity)  # Suppression de l'utilisateur
            return jsonify({'email': email}), 200

        except UserNotFoundError as e:
            return jsonify({"error": str(e)}), 404
