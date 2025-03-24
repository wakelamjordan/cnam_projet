from flask import Blueprint, request, jsonify
from app.services.home_page_content_service import select_all, insert, disponibility_insert, replace, update, delete
from app.validators.home_page_content_validator import insert as insert_validator
from app.errors.service_error import EntryUnavailableError, InvalidEntryError, ResultEmpty
from app.errors.security_error import AccessDenied
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt

home_page_content_blueprint = Blueprint('home_page_content', __name__)


class HomePageContentController():

    @home_page_content_blueprint.route('', methods=['GET'])
    def index():
        """
        Récupère tout le contenu de la page d'accueil.

        Returns:
            JSON: Une liste de tout le contenu de la page d'accueil.
        """
        return select_all()

    @home_page_content_blueprint.route('', methods=['POST'])
    @jwt_required()
    def new_home_page_content():
        """
        Ajoute un nouveau contenu à la page d'accueil.

        Requires:
            - Role 'ROLE_ADMIN'

        Returns:
            JSON: Le contenu de la page d'accueil nouvellement ajouté.

        Raises:
            AccessDenied: Si l'utilisateur n'a pas les droits d'accès nécessaires.
            EntryUnavailableError: Si le contenu n'est pas disponible pour l'insertion.
            InvalidEntryError: Si les données fournies sont invalides.
        """
        data: dict = request.json
        payload: dict = get_jwt()
        try:
            if not 'role' in payload or payload['role'] != 'ROLE_ADMIN':
                raise AccessDenied()
            if not disponibility_insert(data):
                raise EntryUnavailableError()

            if not insert_validator(data):
                raise InvalidEntryError()

            return jsonify({"home_page_content": insert(data)}), 200
        except EntryUnavailableError as e:
            return jsonify({"error": str(e)}), 400
        except InvalidEntryError as e:
            return jsonify({"error": str(e)}), 400
        except AccessDenied as e:
            return jsonify({"error": str(e)}), 403

    @home_page_content_blueprint.route('', methods=['PUT'])
    @jwt_required()
    def put_home_page_content():
        """
        Remplace le contenu existant de la page d'accueil.

        Requires:
            - Role 'ROLE_ADMIN'

        Returns:
            JSON: Le contenu de la page d'accueil mis à jour.

        Raises:
            AccessDenied: Si l'utilisateur n'a pas les droits d'accès nécessaires.
            IntegrityError: Si une contrainte d'intégrité est violée.
            InvalidEntryError: Si les données fournies sont invalides.
        """
        data: dict = request.json
        payload: dict = get_jwt()
        try:
            if not 'role' in payload or payload['role'] != 'ROLE_ADMIN':
                raise AccessDenied()
            if not insert_validator(data['put']):
                raise InvalidEntryError()

            return jsonify({"home_page_content": replace(data)}), 200
        except IntegrityError:
            return jsonify({
                "error":
                "Error due to a unique constraint on the name or element properties."
            }), 400
        except InvalidEntryError as e:
            return jsonify({"error": str(e)}), 400
        except AccessDenied as e:
            return jsonify({"error": str(e)}), 403

    @home_page_content_blueprint.route('', methods=['PATCH'])
    @jwt_required()
    def set_publication_to_home_page_content():
        """
        Met à jour le contenu de la page d'accueil.

        Requires:
            - Role 'ROLE_ADMIN'

        Returns:
            JSON: Un message de confirmation de la mise à jour.

        Raises:
            AccessDenied: Si l'utilisateur n'a pas les droits d'accès nécessaires.
            IntegrityError: Si une contrainte d'intégrité est violée.
            InvalidEntryError: Si les données fournies sont invalides.
            ResultEmpty: Si aucun résultat n'est trouvé pour la mise à jour.
        """
        data: dict = request.json
        payload: dict = get_jwt()
        try:
            if not 'role' in payload or payload['role'] != 'ROLE_ADMIN':
                raise AccessDenied()
            return jsonify({"message": update(data)}), 200
        except IntegrityError:
            return jsonify({
                "error":
                "Error due to a unique constraint on the name or element properties."
            }), 400
        except InvalidEntryError as e:
            return jsonify({"error": str(e)}), 400
        except ResultEmpty as e:
            return jsonify({"error": str(e)}), 404
        except AccessDenied as e:
            return jsonify({"error": str(e)}), 403

    @home_page_content_blueprint.route('', methods=['DELETE'])
    @jwt_required()
    def delete_publication_to_home_page_content():
        """
        Supprime le contenu de la page d'accueil.

        Requires:
            - Role 'ROLE_ADMIN'

        Returns:
            JSON: Un message de confirmation de la suppression.

        Raises:
            AccessDenied: Si l'utilisateur n'a pas les droits d'accès nécessaires.
            IntegrityError: Si une contrainte d'intégrité est violée.
            InvalidEntryError: Si les données fournies sont invalides.
            ResultEmpty: Si aucun résultat n'est trouvé pour la suppression.
        """
        data: dict = request.json
        payload: dict = get_jwt()
        try:
            if not 'role' in payload or payload['role'] != 'ROLE_ADMIN':
                raise AccessDenied()
            return jsonify({"home_page_content": delete(data)}), 200
        except IntegrityError:
            return jsonify({
                "error":
                "Error due to a unique constraint on the name or element properties."
            }), 400
        except InvalidEntryError as e:
            return jsonify({"error": str(e)}), 400
        except ResultEmpty as e:
            return jsonify({"error": str(e)}), 404
        except AccessDenied as e:
            return jsonify({"error": str(e)}), 403
