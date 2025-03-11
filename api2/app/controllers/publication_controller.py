from flask import Blueprint, jsonify, request, Response
from app.services.publication_service import insert, find_all, delete, toggle_on_line, toggle_revision, find_by_slug, replace, copy
from app.errors.user_error import UserNotFoundError
from app.errors.publication_error import (
    PublicationTitleDoesExist, PublicationSlugDoesExist, DataNotValid,
    PublicationNotExist, PublicationIsOnLine, PublicationNotCategory,
    PublicationDataNotValid, PublicationCopyAlreadyExist)
from app.errors.category_error import CategoryNotExist
from app.errors.security_error import AccessDenied
from flask_jwt_extended import jwt_required, get_jwt
from typing import Dict, Any, List

publication_blueprint = Blueprint('publication', __name__)


class PublicationController:

    @staticmethod
    @publication_blueprint.route('/publications', methods=['GET'])
    @jwt_required()
    def _get_all() -> Response:
        """Retrieve all publications. Admins get all, others get their own."""
        payload: Dict[str, Any] = get_jwt()
        result: List[Dict[str, Any]] = find_all(
        ) if payload["role"] == "ROLE_ADMIN" else find_all(payload["sub"])
        return jsonify({"publications": result}), 200

    @staticmethod
    @publication_blueprint.route('/publication/new', methods=['POST'])
    @jwt_required()
    def _new() -> Response:
        """Create a new publication."""
        try:
            data: Dict[str, Any] = request.get_json()
            payload: Dict[str, Any] = get_jwt()
            data["author_email"] = payload["sub"]
            if payload["role"] != "ROLE_ADMIN":
                del data["on_line"]
            return jsonify({"message": insert(data)}), 200
        except (AccessDenied, PublicationTitleDoesExist,
                PublicationSlugDoesExist) as e:
            return jsonify({"error": str(e)}), 403
        except CategoryNotExist as e:
            return jsonify({"error": str(e)}), 404

    @staticmethod
    @publication_blueprint.route('/publication/on_line', methods=['PATCH'])
    @jwt_required()
    def _toggle_on_line() -> Response:
        """Toggle publication online status."""
        try:
            data: Dict[str, Any] = request.get_json()
            payload: Dict[str, Any] = get_jwt()
            if payload["role"] != "ROLE_ADMIN":
                raise AccessDenied()
            return jsonify({"message": toggle_on_line(data)}), 200
        except (AccessDenied, PublicationNotExist,
                PublicationNotCategory) as e:
            return jsonify({"error": str(e)}), e.code

    @staticmethod
    @publication_blueprint.route('/publication/revision', methods=['PATCH'])
    @jwt_required()
    def _toggle_revision() -> Response:
        """Toggle publication revision status."""
        try:
            data: Dict[str, Any] = request.get_json()
            payload: Dict[str, Any] = get_jwt()
            if payload["role"] == "ROLE_ADMIN":
                result: List[Dict[str, Any]] = toggle_revision(data)
            else:
                data["author_email"] = payload["sub"]
                result = toggle_revision(data)
            return jsonify({"publications": result}), 200
        except (AccessDenied, PublicationNotExist) as e:
            return jsonify({"error": str(e)}), e.code

    @staticmethod
    @publication_blueprint.route('/publication/<string:slug>', methods=['GET'])
    @jwt_required()
    def _get_one(slug: str) -> Response:
        """Retrieve a single publication by slug."""
        try:
            payload: Dict[str, Any] = get_jwt()
            data: Dict[str, Any] = {
                "slug": slug,
                "author_email": payload["sub"]
            }
            if "role" in payload and payload["role"] == "ROLE_ADMIN":
                data["role"] = payload["role"]
            entity_find = find_by_slug(data)
            return jsonify(entity_find), 200
        except (PublicationNotExist, AccessDenied) as e:
            return jsonify({"error": str(e)}), e.code

    @staticmethod
    @publication_blueprint.route('/publication/copy', methods=['POST'])
    @jwt_required()
    def _cpy() -> Response:
        """Copy a publication."""
        try:
            payload: Dict[str, Any] = get_jwt()
            if "role" not in payload or payload["role"] != "ROLE_ADMIN":
                raise AccessDenied()
            data: Dict[str, Any] = request.json
            return jsonify({"message": copy(data)}), 200
        except (PublicationCopyAlreadyExist, PublicationNotExist,
                AccessDenied) as e:
            return jsonify({"error": str(e)}), e.code

    @staticmethod
    @publication_blueprint.route('/publication/<string:slug>', methods=['PUT'])
    @jwt_required()
    def _replace(slug: str) -> Response:
        """Replace a publication."""
        try:
            payload: Dict[str, Any] = get_jwt()
            data: Dict[str, Any] = request.json
            data.update({"slug_actual": slug, "user": payload["sub"]})
            required_fields = {
                "title", "slug", "description", "content", "category",
                "author_email"
            }
            if not required_fields.issubset(data.keys()):
                raise PublicationDataNotValid()
            if "role" in payload and payload["role"] == "ROLE_ADMIN":
                data["role"] = payload["role"]
            return jsonify({"message": replace(data)}), 200
        except (PublicationSlugDoesExist, PublicationTitleDoesExist,
                CategoryNotExist, UserNotFoundError, PublicationNotExist,
                AccessDenied, PublicationDataNotValid) as e:
            return jsonify({"error": str(e)}), e.code
        except PublicationIsOnLine:
            return jsonify({"error":
                            "You can't edit publication on line."}), 403

    @staticmethod
    @publication_blueprint.route('/publication/delete', methods=['DELETE'])
    @jwt_required()
    def _delete() -> Response:
        """Delete a publication."""
        try:
            data: Dict[str, Any] = request.json
            payload: Dict[str, Any] = get_jwt()
            if "role" not in payload or payload["role"] != "ROLE_ADMIN":
                data["author_email"] = payload["sub"]
            result: str = delete(data)
            return jsonify({'delete': result}), 200
        except (PublicationNotExist, DataNotValid, AccessDenied,
                PublicationIsOnLine) as e:
            return jsonify({"error": str(e)}), e.code
