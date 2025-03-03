from app.models import get_db
from app.models.user_model import User as Entity
from sqlalchemy.orm import Session
from app.errors.user_error import UserNotFoundError, UserEmailDoesExist, UserEmailNotValide


def insert(entity_dict: dict) -> str:
    """
    Insère un nouvel utilisateur dans la base de données.

    Paramètres:
        entity_dict (dict) : Dictionnaire contenant les informations de l'utilisateur à insérer.

    Retourne:
        str : L'email de l'utilisateur inséré.

    Lève:
        UserEmailDoesExist : Si l'email existe déjà.
        UserEmailNotValide : Si l'email n'est pas valide.
    """
    db: Session = next(get_db())

    try:
        check_email = db.query(Entity).filter(
            Entity._email == entity_dict["email"]).first()
        if check_email is not None:
            raise UserEmailDoesExist()
        entity: Entity = Entity(entity_dict["email"])
        entity.set_password(entity_dict["password"])
        db.add(entity)
        db.commit()
    except UserEmailDoesExist:
        db.rollback()
        raise
    except UserEmailNotValide:
        db.rollback()
        raise
    finally:
        db.close()

    return entity_dict["email"]


def delete(entity_dict: dict) -> str:
    """
    Supprime un utilisateur de la base de données en fonction de son email.

    Paramètres:
        entity_dict (dict) : Dictionnaire contenant l'email de l'utilisateur à supprimer.

    Retourne:
        str : L'email de l'utilisateur supprimé.

    Lève:
        UserNotFoundError : Si l'utilisateur n'est pas trouvé.
    """
    db: Session = next(get_db())
    try:
        entity_find = db.query(Entity).filter(
            Entity._email == entity_dict["email"]).first()
        if not entity_find:
            raise UserNotFoundError()
        db.delete(entity_find)
        db.commit()
        return entity_dict["email"]
    except UserNotFoundError:
        db.rollback()
        raise
    finally:
        db.close()


def find_by_email(entity_dict: dict) -> dict:
    """
    Trouve un utilisateur dans la base de données en fonction de son email.

    Paramètres:
        entity_dict (dict) : Dictionnaire contenant l'email de l'utilisateur à rechercher.

    Retourne:
        dict : Les informations de l'utilisateur trouvé, sans le mot de passe.

    Lève:
        UserNotFoundError : Si l'utilisateur n'est pas trouvé.
    """
    db: Session = next(get_db())
    try:
        entity = db.query(Entity).filter(
            Entity._email == entity_dict["email"]).first()
        if not entity:
            raise UserNotFoundError()
        result = entity.to_dict()
        del result["password"]
        return result
    except:
        db.rollback()
        raise


def find_all() -> list:
    """
    Récupère tous les utilisateurs de la base de données.

    Retourne:
        list : Une liste de dictionnaires contenant les informations des utilisateurs, sans les mots de passe.

    Lève:
        Exception : En cas d'erreur lors de la récupération des utilisateurs.
    """
    db: Session = next(get_db())
    try:
        entities = db.query(Entity).all()
        for i in range(len(entities)):
            entities[i] = entities[i].to_dict()
            del entities[i]["password"]
        db.commit()
        return entities
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")
    finally:
        db.close()


def replace(entity_dict: dict, email: str) -> dict:
    """
    Remplace les informations d'un utilisateur existant dans la base de données.

    Paramètres:
        entity_dict (dict) : Dictionnaire contenant les nouvelles informations de l'utilisateur.
        email (str) : L'email de l'utilisateur à mettre à jour.

    Retourne:
        dict : Les nouvelles informations de l'utilisateur, sans le mot de passe et certaines autres informations sensibles.

    Lève:
        UserNotFoundError : Si l'utilisateur n'est pas trouvé.
    """
    db: Session = next(get_db())
    try:
        entity_to_update: Entity = db.query(Entity).filter(
            Entity._email == email).first()
        if entity_to_update is None:
            raise UserNotFoundError()

        # Mise à jour des champs si fournis
        entity_to_update.set_email(entity_dict["email"])
        entity_to_update.set_role(entity_dict["role"])
        entity_to_update.set_password(entity_dict["password"])
        entity_to_update.set_lastname(entity_dict["lastname"])
        entity_to_update.set_firstname(entity_dict["firstname"])
        entity_to_update.set_birth_at(entity_dict["birth_at"])

        # Appliquer les modifications
        entity_dict: dict = entity_to_update.to_dict()
        db.add(entity_to_update)
        db.commit()
        del entity_dict["password"]
        del entity_dict["created_at"]
        del entity_dict["login_at"]

        return entity_dict
    except UserNotFoundError:
        raise
    finally:
        db.close()


def update(entity_dict: dict, email: str) -> dict:
    """
    Met à jour les informations d'un utilisateur existant dans la base de données.

    Paramètres:
        entity_dict (dict) : Dictionnaire contenant les informations à mettre à jour.
        email (str) : L'email de l'utilisateur à mettre à jour.

    Retourne:
        dict : Les informations mises à jour de l'utilisateur, sans le mot de passe.

    Lève:
        UserNotFoundError : Si l'utilisateur n'est pas trouvé.
    """
    db: Session = next(get_db())
    try:
        entity_to_update: Entity = db.query(Entity).filter(
            Entity._email == email).first()
        if entity_to_update is None:
            raise UserNotFoundError()

        # Mise à jour des champs si fournis
        if "email" in entity_dict and entity_dict[
                "email"] != entity_to_update.get_email():
            entity_to_update.set_email(entity_dict["email"])

        if "password" in entity_dict and entity_dict[
                "password"] != entity_to_update.get_password():
            entity_to_update.set_password(entity_dict["password"])

        if "role" in entity_dict and entity_dict[
                "role"] != entity_to_update.get_role():
            entity_to_update.set_role(entity_dict["role"])

        if "firstname" in entity_dict and entity_dict[
                "firstname"] != entity_to_update.get_firstname():
            entity_to_update.set_firstname(entity_dict["firstname"])

        if "lastname" in entity_dict and entity_dict[
                "lastname"] != entity_to_update.get_lastname():
            entity_to_update.set_lastname(entity_dict["lastname"])

        if "birth_at" in entity_dict and entity_dict[
                "birth_at"] != entity_to_update.get_birth_at():
            entity_to_update.set_birth_at(entity_dict["birth_at"])

        # Appliquer les modifications
        entity_update_dict: dict = entity_to_update.to_dict()
        db.add(entity_to_update)
        db.commit()
        del entity_update_dict["password"]
        return entity_update_dict

    except UserNotFoundError:
        raise
    finally:
        db.close()
