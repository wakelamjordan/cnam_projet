from app.models import get_db
from app.models.publication_model import Publication as Entity
from sqlalchemy.orm import Session
from app.errors.publication_error import PublicationSlugDoesExist, PublicationTitleDoesExist, PublicationNotExist, PublicationIsOnLine


def insert(entity_dict: dict) -> str:
    db: Session = next(get_db())

    try:
        # vérification de la disponibilité du title et du slug
        check_title = db.query(Entity).filter(
            Entity._title == entity_dict["title"]).first()
        if check_title is not None:
            raise PublicationTitleDoesExist()
        check_slug = db.query(Entity).filter(
            Entity._slug == entity_dict["slug"]).first()
        if check_slug is not None:
            raise PublicationSlugDoesExist()
        if not "on_line" in entity_dict:
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

        db.add(entity)
        db.commit()

        return entity.get_slug()
        # return entity_dict["email"]
    except PublicationTitleDoesExist:
        db.rollback()
        raise
    except PublicationSlugDoesExist:
        db.rollback()
        raise
    finally:
        db.close()


def delete(entity_dict: dict) -> str:
    # return entity_dict["author_email"]
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

        if entity_find.get_on_line() == True:
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
    # return entity_dict["author_email"]
    db: Session = next(get_db())
    try:
        # if "author_email" in entity_dict:
        entity_find = db.query(Entity).filter(
            Entity._title == entity_dict["title"]).first()
        # else:
        #     entity_find = db.query(Entity).filter(
        #         Entity._title == entity_dict["title"]).first()
        if not entity_find:
            raise PublicationNotExist()

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
    # return entity_dict["author_email"]
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
        # return entity_find.to_dict()
        return entity_find.get_slug()
    except PublicationNotExist:
        db.rollback()
        raise
    finally:
        db.close()


def find_by_slug(entity_dict: dict) -> dict:
    db: Session = next(get_db())
    try:
        entity = db.query(Entity).filter(
            Entity._slug == entity_dict["slug"]).first()
        if not entity:
            raise PublicationNotExist()
        if "role" in entity_dict and entity_dict["role"] == "ROLE_ADMIN":
            return entity.to_dict()
        elif entity.get_author_email() == entity_dict["author_email"]:
            return entity.to_dict()
        # elif not entity.get_on_line():
        raise PublicationNotExist()
        # return entity.to_dict()
    except:
        db.rollback()
        raise


def find_all(user_email: str = None) -> list:
    db: Session = next(get_db())
    try:
        if not user_email:
            entities = db.query(Entity).all()
        else:
            entities = db.query(Entity).filter(
                Entity._author_email == user_email).all()
        for i in range(len(entities)):
            entities[i] = entities[i].to_dict()
            # del entities[i]["password"]
        db.commit()
        return entities
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")
    finally:
        db.close()


# def replace(entity_dict: dict, email: str) -> dict:
#     """
#     Replaces the information of an existing user in the database.

#     Parameters:
#         entity_dict (dict): A dictionary containing the new information of the user.
#         email (str): The email of the user to be updated.

#     Returns:
#         dict: The updated user information, excluding the password and certain sensitive information.

#     Raises:
#         UserNotFoundError: If the user is not found.
#     """
#     db: Session = next(get_db())
#     try:
#         entity_to_update: Entity = db.query(Entity).filter(
#             Entity._email == email).first()
#         if entity_to_update is None:
#             raise UserNotFoundError()

#         # Update fields if provided
#         entity_to_update.set_email(entity_dict["email"])
#         entity_to_update.set_role(entity_dict["role"])
#         entity_to_update.set_password(entity_dict["password"])
#         entity_to_update.set_lastname(entity_dict["lastname"])
#         entity_to_update.set_firstname(entity_dict["firstname"])
#         entity_to_update.set_birth_at(entity_dict["birth_at"])

#         # Apply changes
#         entity_dict: dict = entity_to_update.to_dict()
#         db.add(entity_to_update)
#         db.commit()
#         del entity_dict["password"]
#         del entity_dict["created_at"]
#         del entity_dict["login_at"]

#         return entity_dict
#     except UserNotFoundError:
#         raise
#     finally:
#         db.close()

# def update(entity_dict: dict, email: str) -> dict:
#     """
#     Updates the information of an existing user in the database.

#     Parameters:
#         entity_dict (dict): A dictionary containing the information to be updated.
#         email (str): The email of the user to be updated.

#     Returns:
#         dict: The updated user information, excluding the password.

#     Raises:
#         UserNotFoundError: If the user is not found.
#     """
#     db: Session = next(get_db())
#     try:
#         entity_to_update: Entity = db.query(Entity).filter(
#             Entity._email == email).first()
#         if entity_to_update is None:
#             raise UserNotFoundError()

#         # Update fields if provided
#         if "email" in entity_dict and entity_dict[
#                 "email"] != entity_to_update.get_email():
#             entity_to_update.set_email(entity_dict["email"])

#         if "password" in entity_dict and entity_dict[
#                 "password"] != entity_to_update.get_password():
#             entity_to_update.set_password(entity_dict["password"])

#         if "role" in entity_dict and entity_dict[
#                 "role"] != entity_to_update.get_role():
#             entity_to_update.set_role(entity_dict["role"])

#         if "firstname" in entity_dict and entity_dict[
#                 "firstname"] != entity_to_update.get_firstname():
#             entity_to_update.set_firstname(entity_dict["firstname"])

#         if "lastname" in entity_dict and entity_dict[
#                 "lastname"] != entity_to_update.get_lastname():
#             entity_to_update.set_lastname(entity_dict["lastname"])

#         if "birth_at" in entity_dict and entity_dict[
#                 "birth_at"] != entity_to_update.get_birth_at():
#             entity_to_update.set_birth_at(entity_dict["birth_at"])

#         # Apply changes
#         entity_update_dict: dict = entity_to_update.to_dict()
#         db.add(entity_to_update)
#         db.commit()
#         del entity_update_dict["password"]
#         return entity_update_dict

#     except UserNotFoundError:
#         raise
#     finally:
#         db.close()
