from flask import Blueprint, request, jsonify
from app.services.category_service import find_all, insert, delete, put
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt
from app.errors.category_error import CategoryNotValid, CategoryNotExist, CategoryAlreadyExist, CategoryHavePublication, CategoryHaveSub
from app.errors.role_error import RoleNotFoundError
from app.errors.security_error import AccessDenied

category_blueprint = Blueprint("category", __name__)


class CategoryController:

    @staticmethod
    @category_blueprint.route('', methods=['GET'])
    def categories():
        """
        Récupère toutes les catégories.

        Vérifie si un jeton JWT est présent dans l'en-tête de la requête. Si c'est le cas,
        vérifie le rôle de l'utilisateur et retourne les catégories en fonction du rôle.
        Sinon, retourne toutes les catégories.

        Returns:
            Response: Liste des catégories en JSON.
        """
        auth_header = request.headers.get('Authorization')
        if auth_header:
            verify_jwt_in_request()
            payload: dict = get_jwt()
            return find_all(payload['role'])
        else:
            return find_all()

    @staticmethod
    @category_blueprint.route('', methods=['POST'])
    @jwt_required()
    def category_new():
        """
        Crée une nouvelle catégorie.

        Vérifie si l'utilisateur a le rôle 'ROLE_ADMIN'. Si oui, insère une nouvelle catégorie
        à partir des données JSON fournies dans la requête.

        Returns:
            Response: La catégorie créée en JSON avec un statut HTTP 200.

        Raises:
            CategoryNotValid: Si la catégorie n'est pas valide.
            ValueError: Si les données fournies sont incorrectes.
            CategoryAlreadyExist: Si la catégorie existe déjà.
            CategoryNotExist: Si la catégorie n'existe pas.
            RoleNotFoundError: Si le rôle n'est pas trouvé.
            AccessDenied: Si l'accès est refusé.
        """
        try:
            payload: dict = get_jwt()
            if not 'role' in payload or payload['role'] != 'ROLE_ADMIN':
                raise AccessDenied()
            category: dict = request.json

            return jsonify({'category': insert(category)}), 200
        except CategoryNotValid as e:
            return jsonify({"error": str(e)}), 415
        except ValueError as e:
            return jsonify({"error": str(e)}), 415
        except CategoryAlreadyExist as e:
            return jsonify({"error": str(e)}), 400
        except CategoryNotExist as e:
            return jsonify({"error": str(e)}), 404
        except RoleNotFoundError as e:
            return jsonify({"error": str(e)}), 404
        except AccessDenied as e:
            return jsonify({"error": str(e)}), 403

    @staticmethod
    @category_blueprint.route('', methods=['DELETE'])
    @jwt_required()
    def category_delete():
        """
        Supprime une catégorie.

        Vérifie si l'utilisateur a le rôle 'ROLE_ADMIN'. Si oui, supprime la catégorie
        spécifiée dans les données JSON de la requête.

        Returns:
            Response: La catégorie supprimée en JSON avec un statut HTTP 200.

        Raises:
            CategoryHaveSub: Si la catégorie a des sous-catégories.
            CategoryHavePublication: Si la catégorie a des publications.
            CategoryNotExist: Si la catégorie n'existe pas.
            AccessDenied: Si l'accès est refusé.
        """
        try:
            payload: dict = get_jwt()
            if not 'role' in payload or payload['role'] != 'ROLE_ADMIN':
                raise AccessDenied()
            category: dict = request.json
            return jsonify({'category': delete(category)}), 200
        except CategoryHaveSub as e:
            return jsonify({"error": str(e)}), 400
        except CategoryHavePublication as e:
            return jsonify({"error": str(e)}), 400
        except CategoryNotExist as e:
            return jsonify({"error": str(e)}), 404
        except AccessDenied as e:
            return jsonify({"error": str(e)}), 403

    @staticmethod
    @category_blueprint.route('', methods=['PUT'])
    @jwt_required()
    def category_put():
        """
        Met à jour une catégorie existante.

        Vérifie si l'utilisateur a le rôle 'ROLE_ADMIN'. Si oui, met à jour la catégorie
        spécifiée dans les données JSON de la requête.

        Returns:
            Response: La catégorie mise à jour en JSON avec un statut HTTP 200.

        Raises:
            CategoryNotValid: Si la catégorie n'est pas valide.
            CategoryHavePublication: Si la catégorie a des publications.
            CategoryNotExist: Si la catégorie n'existe pas.
            RoleNotFoundError: Si le rôle n'est pas trouvé.
            AccessDenied: Si l'accès est refusé.
        """
        try:
            payload: dict = get_jwt()
            if not 'role' in payload or payload['role'] != 'ROLE_ADMIN':
                raise AccessDenied()
            category: dict = request.json
            return jsonify({'category': put(category)}), 200
        except CategoryNotValid as e:
            return jsonify({"error": str(e)}), 400
        except CategoryHavePublication as e:
            return jsonify({"error": str(e)}), 400
        except CategoryNotExist as e:
            return jsonify({"error": str(e)}), 404
        except RoleNotFoundError as e:
            return jsonify({"error": str(e)}), 404
        except AccessDenied as e:
            return jsonify({"error": str(e)}), 403
