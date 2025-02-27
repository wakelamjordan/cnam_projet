from app.models import get_db
from app.models.user_model import User as Entity
from sqlalchemy.orm import Session
from app.errors.user_error import UserNotFoundError, UserEmailDoesExist, UserEmailNotValide


def insert(entity_dict: dict) -> str:
    """
    Insère un nouvel utilisateur dans la base de données.

    Paramètres:
        entity (Entity) : L'utilisateur à insérer.

    Retourne:
        str : L'email de l'utilisateur inséré.

    Lève:
        UserEmailDoesExist : Si l'email existe déjà.
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
    db: Session = next(get_db())
    try:
        # entity_find = find_by_email(entity_dict["email"])
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
    db: Session = next(get_db())
    try:
        entitys = db.query(Entity).all()
        for i in range(len(entitys)):
            entitys[i] = entitys[i].to_dict()
            del entitys[i]["password"]
        db.commit()
        return entitys
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")
    finally:
        db.close()


def replace(entity_dict: dict, email: str) -> dict:
    db: Session = next(get_db())
    try:
        entity_to_update: Entity = db.query(Entity).filter(
            Entity._email == email).first()
        if entity_to_update is None:
            raise UserNotFoundError()

        # 🔹 Mise à jour des champs si fournis

        entity_to_update.set_email(entity_dict["email"])

        entity_to_update.set_role(entity_dict["role"])

        entity_to_update.set_password(entity_dict["password"])

        entity_to_update.set_lastname(entity_dict["lastname"])

        entity_to_update.set_firstname(entity_dict["firstname"])

        entity_to_update.set_birth_at(entity_dict["birth_at"])

        # ✅ Appliquer les modifications
        entity_dict: dict = entity_to_update.to_dict()
        db.add(entity_to_update)
        db.commit()
        db.refresh(entity_to_update
                   )  # Rafraîchir pour récupérer les nouvelles valeurs
        # entity_dict: dict = entity_to_update.to_dict()
        return entity_dict
    except UserNotFoundError:
        raise
    finally:
        db.close()


def update(entity_dict: dict, email: str) -> Entity:
    db: Session = next(get_db())
    try:
        entity_to_update: Entity = db.query(Entity).filter(
            Entity._email == email).first()
        if entity_to_update is None:
            raise UserNotFoundError()

        # 🔹 Mise à jour des champs si fournis
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

        # ✅ Appliquer les modifications
        entity_update_dict: dict = entity_to_update.to_dict()
        db.add(entity_to_update)
        db.commit()
        db.refresh(entity_to_update
                   )  # Rafraîchir pour récupérer les nouvelles valeurs
        del entity_update_dict["password"]
        return entity_update_dict

    except UserNotFoundError:
        raise
    finally:
        db.close()
