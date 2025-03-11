from app.models import get_db
from app.models.publication_model import Publication as Entity
from app.models.category_model import Category
from app.models.user_model import User
from sqlalchemy.orm import Session
from app.errors.publication_error import (
    PublicationSlugDoesExist, PublicationTitleDoesExist, PublicationNotExist,
    PublicationIsOnLine, PublicationNotCategory, PublicationCopyAlreadyExist)
from app.errors.user_error import UserNotFoundError
from app.errors.category_error import CategoryNotExist
from app.errors.security_error import AccessDenied


def insert(entity_dict: dict) -> str:
    """
    Insert a new publication into the database.

    Args:
        entity_dict (dict): A dictionary containing the publication details.

    Returns:
        str: The slug of the newly inserted publication.

    Raises:
        PublicationTitleDoesExist: If a publication with the same title already exists.
        PublicationSlugDoesExist: If a publication with the same slug already exists.
        CategoryNotExist: If the specified category does not exist.
    """
    db: Session = next(get_db())

    try:
        check_title: Entity = db.query(Entity).filter(
            Entity._title == entity_dict["title"]).first()

        if "category" in entity_dict:
            check_category: Category = db.query(Category).filter(
                Category._name == entity_dict["category"]).first()
            if not check_category:
                raise CategoryNotExist()
        else:
            entity_dict["category"] = None

        if check_title is not None:
            raise PublicationTitleDoesExist()

        check_slug = db.query(Entity).filter(
            Entity._slug == entity_dict["slug"]).first()
        if check_slug is not None:
            raise PublicationSlugDoesExist()

        if "on_line" not in entity_dict:
            entity_dict["on_line"] = False

        entity: Entity = Entity(
            entity_dict["title"],
            entity_dict["slug"],
            entity_dict["description"],
            entity_dict["content"],
            entity_dict["on_line"],
            entity_dict["revision"],
            entity_dict["author_email"],
            entity_dict["category"],
        )

        entity.set_updated_at()

        db.add(entity)
        db.commit()

        return entity.get_slug()

    except PublicationTitleDoesExist:
        db.rollback()
        raise
    except PublicationSlugDoesExist:
        db.rollback()
        raise
    except CategoryNotExist:
        db.rollback()
        raise
    finally:
        db.close()


def copy(entity_dict: dict) -> str:
    """
    Create a copy of an existing publication.

    Args:
        entity_dict (dict): A dictionary containing the publication details.

    Returns:
        str: The slug of the copied publication.

    Raises:
        PublicationCopyAlreadyExist: If a copy of the publication already exists.
        PublicationNotExist: If the publication to be copied does not exist.
    """
    db: Session = next(get_db())
    try:
        entity_find: Entity = db.query(Entity).filter(
            Entity._title == entity_dict["title"]).first()
        entity_already_copy: Entity = db.query(Entity).filter(
            Entity._title == entity_dict["title"] + "-copy").first()

        if entity_already_copy:
            raise PublicationCopyAlreadyExist(
                f"Publication copy already exists, last updated {entity_already_copy.get_updated_at()}."
            )
        if not entity_find:
            raise PublicationNotExist()

        entity_copie: Entity = Entity(
            entity_find.get_title() + "-copy",
            entity_find.get_slug() + "-copy",
            entity_find.get_description(),
            entity_find.get_content(),
            author_email=entity_find.get_author_email(),
            category=entity_find.get_category())
        entity_copie.set_updated_at()
        db.add(entity_copie)
        db.commit()

        return entity_copie.get_slug()
    except PublicationNotExist:
        db.rollback()
        raise
    finally:
        db.close()


def replace(entity_dict: dict) -> str:
    """
    Replace an existing publication with new details.

    Args:
        entity_dict (dict): A dictionary containing the new publication details.

    Returns:
        str: The slug of the updated publication.

    Raises:
        PublicationIsOnLine: If the publication is currently online.
        PublicationNotExist: If the publication to be replaced does not exist.
        PublicationTitleDoesExist: If a publication with the new title already exists.
        PublicationSlugDoesExist: If a publication with the new slug already exists.
        CategoryNotExist: If the specified category does not exist.
        UserNotFoundError: If the new author does not exist.
        AccessDenied: If the user does not have permission to make the change.
    """
    db: Session = next(get_db())

    try:
        entity_find: Entity = db.query(Entity).filter(
            Entity._slug == entity_dict["slug_actual"]).first()
        if entity_find.get_on_line():
            raise PublicationIsOnLine()

        flag_is_admin: bool = entity_dict.get("role") == "ROLE_ADMIN"
        flag_is_author: bool = entity_dict[
            "user"] == entity_find.get_author_email()

        if not flag_is_admin and not flag_is_author:
            raise PublicationNotExist()

        if entity_find.get_title() != entity_dict[
                "title"] or entity_find.get_slug() != entity_dict["slug"]:
            if entity_find.get_title() != entity_dict["title"] and db.query(
                    Entity).filter(
                        Entity._title == entity_dict["title"]).first():
                raise PublicationTitleDoesExist()
            if entity_find.get_slug() != entity_dict["slug"] and db.query(
                    Entity).filter(
                        Entity._slug == entity_dict["slug"]).first():
                raise PublicationSlugDoesExist()
            return "titre différent"

        if entity_find.get_category() != entity_dict["category"]:
            if not db.query(Category).filter(
                    Category._name == entity_dict["category"]).first(
                    ) and entity_dict["category"] is not None:
                raise CategoryNotExist()

        new_author: User = db.query(User).filter(
            User._email == entity_dict["author_email"]).first()
        if not new_author and flag_is_admin:
            raise UserNotFoundError()
        if not new_author and flag_is_author:
            raise AccessDenied()
        if not flag_is_admin and entity_dict["author_email"] != entity_dict[
                "user"]:
            raise AccessDenied()

        entity_find.set_title(entity_dict["title"])
        entity_find.set_slug(entity_dict["slug"])
        entity_find.set_description(entity_dict["description"])
        entity_find.set_content(entity_dict["content"])
        entity_find.set_author_email(entity_dict["author_email"])
        entity_find.set_category(entity_dict["category"])

        entity_find.set_updated_at()

        db.add(entity_find)
        db.commit()
        return entity_find.get_slug()
    except UserNotFoundError:
        db.rollback()
        raise
    except PublicationTitleDoesExist:
        db.rollback()
        raise
    except PublicationSlugDoesExist:
        db.rollback()
        raise
    except CategoryNotExist:
        db.rollback()
        raise
    except PublicationNotExist:
        db.rollback()
        raise
    except AccessDenied:
        db.rollback()
        raise
    finally:
        db.close()


def delete(entity_dict: dict) -> str:
    """
    Delete a publication from the database.

    Args:
        entity_dict (dict): A dictionary containing the publication details.

    Returns:
        str: The slug of the deleted publication.

    Raises:
        PublicationNotExist: If the publication to be deleted does not exist.
        PublicationIsOnLine: If the publication is currently online.
    """
    db: Session = next(get_db())
    try:
        if "author_email" in entity_dict:
            entity_find = db.query(Entity).filter(
                Entity._author_email == entity_dict["author_email"],
                Entity._title == entity_dict["title"]).first()
        else:
            entity_find = db.query(Entity).filter(
                Entity._title == entity_dict["title"]).first()

        if not entity_find:
            raise PublicationNotExist()

        if entity_find.get_on_line():
            raise PublicationIsOnLine()

        db.delete(entity_find)
        db.commit()
        return entity_find.get_slug()
    except PublicationNotExist:
        db.rollback()
        raise
    finally:
        db.close()


def toggle_on_line(entity_dict: dict) -> str:
    """
    Toggle the online status of a publication.

    Args:
        entity_dict (dict): A dictionary containing the publication details.

    Returns:
        str: The slug of the updated publication.

    Raises:
        PublicationNotExist: If the publication does not exist.
        PublicationNotCategory: If the publication does not have a category.
    """
    db: Session = next(get_db())
    try:
        entity_find = db.query(Entity).filter(
            Entity._title == entity_dict["title"]).first()

        if not entity_find:
            raise PublicationNotExist()
        if not entity_find.get_category():
            raise PublicationNotCategory()

        entity_find.set_on_line(not entity_find.get_on_line())
        entity_find.set_revision(False)

        db.add(entity_find)
        db.commit()
        return entity_find.get_slug()
    except PublicationNotExist:
        db.rollback()
        raise
    finally:
        db.close()


def toggle_revision(entity_dict: dict) -> str:
    """
    Toggle the revision status of a publication.

    Args:
        entity_dict (dict): A dictionary containing the publication details.

    Returns:
        str: The slug of the updated publication.

    Raises:
        PublicationNotExist: If the publication does not exist.
    """
    db: Session = next(get_db())
    try:
        if "author_email" in entity_dict:
            entity_find = db.query(Entity).filter(
                Entity._title == entity_dict["title"],
                Entity._author_email == entity_dict["author_email"]).first()
        else:
            entity_find = db.query(Entity).filter(
                Entity._title == entity_dict["title"]).first()

        if not entity_find:
            raise PublicationNotExist()

        entity_find.set_revision(not entity_find.get_revision())

        db.add(entity_find)
        db.commit()

        return entity_find.get_slug()
    except PublicationNotExist:
        db.rollback()
        raise
    finally:
        db.close()


def find_by_slug(entity_dict: dict) -> dict:
    """
    Find a publication by its slug.

    Args:
        entity_dict (dict): A dictionary containing the slug and optional role.

    Returns:
        dict: The publication details as a dictionary.

    Raises:
        PublicationNotExist: If the publication does not exist or the user does not have access.
    """
    db: Session = next(get_db())
    try:
        entity = db.query(Entity).filter(
            Entity._slug == entity_dict["slug"]).first()
        if not entity:
            raise PublicationNotExist()
        if entity_dict.get("role") == "ROLE_ADMIN" or entity.get_author_email(
        ) == entity_dict["author_email"]:
            return entity.to_dict()

        raise PublicationNotExist()
    except:
        db.rollback()
        raise
    finally:
        db.close()


def find_all(user_email: str = None) -> list:
    """
    Find all publications, optionally filtered by user email.

    Args:
        user_email (str, optional): The email of the user to filter publications by. Defaults to None.

    Returns:
        list: A list of publication details as dictionaries.

    Raises:
        Exception: If an error occurs during the database query.
    """
    db: Session = next(get_db())
    try:
        if not user_email:
            entities = db.query(Entity).all()
        else:
            entities = db.query(Entity).filter(
                Entity._author_email == user_email).all()

        return [entity.to_dict() for entity in entities]
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")
    finally:
        db.close()
