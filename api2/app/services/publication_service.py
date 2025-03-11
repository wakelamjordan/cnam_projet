from app.models import get_db
from app.models.publication_model import Publication as Entity
from app.models.category_model import Category
from app.models.user_model import User
from sqlalchemy.orm import Session
from app.errors.publication_error import PublicationSlugDoesExist, PublicationTitleDoesExist, PublicationNotExist, PublicationIsOnLine, PublicationNotCategory, PublicationCopyAlreadyExist, PublicationDoesExist
from app.errors.user_error import UserNotFoundError
from app.errors.category_error import CategoryNotExist
from app.errors.security_error import AccessDenied


def insert(entity_dict: dict) -> str:
    db: Session = next(get_db())

    try:
        # vérification de la disponibilité du title et du slug
        check_title: Entity = db.query(Entity).filter(
            Entity._title == entity_dict["title"]).first()
        # check catégory
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

        entity.set_updated_at()

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
    except CategoryNotExist:
        db.rollback()
        raise
    finally:
        db.close()


def copy(entity_dict: dict):
    db = next(get_db())
    try:
        entity_find: Entity = db.query(Entity).filter(
            Entity._title == entity_dict["title"]).first()
        # vérifier si une copie existe déjà
        entity_already_copy: Entity = db.query(Entity).filter(
            Entity._title == entity_dict["title"] + "-copy").first()
        if entity_already_copy:
            raise PublicationCopyAlreadyExist(
                f"Publication copy already exist last updated {entity_already_copy.get_updated_at()}."
            )
        if not entity_find:
            raise PublicationNotExist()
        # création d'un entité identique avec copie dans les noms et slug
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
    db: Session = next(get_db())

    try:
        #récupération de la publication à modifier
        entity_find: Entity = db.query(Entity).filter(
            Entity._slug == entity_dict["slug_actual"]).first()
        if entity_find.get_on_line():
            raise PublicationIsOnLine()
        # vérification si nouveau slug et titre sont toujours ceux de l'entité à modifier
        # flag_check_title_slug_ok: bool = False
        # if entity_find.get_title() == entity_dict[
        #         "title"] and entity_find.get_slug() == entity_dict["slug"]:
        #     flag_check_title_slug_ok = True
        # # sinon si le titre n'existe pas en bdd c'est ok
        # elif db.query(Entity).filter(
        #         Entity._title == entity_dict["title"]).first():
        #     raise PublicationTitleDoesExist()
        # elif db.query(Entity).filter(
        #         Entity._title == entity_dict["slug"]).first():
        #     raise PublicationSlugDoesExist()
        # else:
        #     flag_check_title_slug_ok = True

        # vérification si autorisé à put

        flag_is_admin: bool = False
        flag_is_author: bool = False

        if 'role' in entity_dict and entity_dict["role"] == "ROLE_ADMIN":
            flag_is_admin = True

        if entity_dict["user"] == entity_find.get_author_email():
            flag_is_author = True

        # flag_user_ok_to_put: bool = False
        if not flag_is_admin and not flag_is_author:
            raise PublicationNotExist()

        # vérifier si les données slug et title sont les même que l'entité que l'on souhaite modifié parce que si oui on a pas besoin d'éffectuer le check de disponibilité en bdd

        if entity_find.get_title() != entity_dict[
                "title"] or entity_find.get_slug() != entity_dict["slug"]:
            # vérifier si titre disponible
            #vérifier si le titre n'es pas le même que la publi trouvé
            if entity_find.get_title() != entity_dict["title"] and db.query(
                    Entity).filter(
                        Entity._title == entity_dict["title"]).first():
                raise PublicationTitleDoesExist()
            if entity_find.get_slug() != entity_dict["slug"] and db.query(
                    Entity).filter(
                        Entity._slug == entity_dict["slug"]).first():
                raise PublicationSlugDoesExist()
            return "titre différent"

        # si catégory différente
        if entity_find.get_category() != entity_dict["category"]:
            # vérifier si catégory valide donc existe
            if not db.query(Category).filter(
                    Category._name == entity_dict["category"]).first(
                    ) and entity_dict["category"] != None:
                raise CategoryNotExist()

        # # vérifier si l'auteur est put
        # if "author_email" in entity_dict:
        new_author: User = db.query(User).filter(
            User._email == entity_dict["author_email"]).first()
        if not new_author and flag_is_admin:
            raise UserNotFoundError()
        if not new_author and flag_is_author:
            raise AccessDenied()
        if not flag_is_admin and entity_dict["author_email"] != entity_dict[
                "user"]:
            raise AccessDenied()

        # entity: Entity = Entity(title=entity_dict["title"],
        #                         slug=entity_dict["slug"],
        #                         description=entity_dict["description"],
        #                         content=entity_dict["content"],
        #                         author_email=entity_dict["author_email"],
        #                         category=entity_dict["category"])

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
        # return entity_find.to_dict()
        return entity.get_slug()
        # return entity_dict["email"]
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
