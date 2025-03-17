from app.models import get_db
from app.models.user_model import User as Entity
from sqlalchemy.orm import Session
from app.errors.user_error import UserNotFoundError, UserEmailDoesExist, UserEmailNotValide


def insert(entity_dict: dict) -> str:
    """
    Inserts a new user into the database.

    Parameters:
        entity_dict (dict): A dictionary containing the user's information to be inserted.

    Returns:
        str: The email of the newly inserted user.

    Raises:
        UserEmailDoesExist: If the email already exists.
        UserEmailNotValide: If the email is invalid.
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

        return entity_dict["email"]
    except UserEmailDoesExist:
        db.rollback()
        raise
    except UserEmailNotValide:
        db.rollback()
        raise
    finally:
        db.close()


def delete(entity_dict: dict) -> str:
    """
    Deletes a user from the database based on their email.

    Parameters:
        entity_dict (dict): A dictionary containing the email of the user to be deleted.

    Returns:
        str: The email of the deleted user.

    Raises:
        UserNotFoundError: If the user is not found.
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
    Finds a user in the database based on their email.

    Parameters:
        entity_dict (dict): A dictionary containing the email of the user to search for.

    Returns:
        dict: The user's information, excluding the password.

    Raises:
        UserNotFoundError: If the user is not found.
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
    Retrieves all users from the database.

    Returns:
        list: A list of dictionaries containing the users' information, excluding the passwords.

    Raises:
        Exception: If an error occurs while retrieving the users.
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
    Replaces the information of an existing user in the database.

    Parameters:
        entity_dict (dict): A dictionary containing the new information of the user.
        email (str): The email of the user to be updated.

    Returns:
        dict: The updated user information, excluding the password and certain sensitive information.

    Raises:
        UserNotFoundError: If the user is not found.
    """
    db: Session = next(get_db())
    try:
        entity_to_update: Entity = db.query(Entity).filter(
            Entity._email == email).first()
        if entity_to_update is None:
            raise UserNotFoundError()

        # Update fields if provided
        entity_to_update.set_email(entity_dict["email"])
        entity_to_update.set_role(entity_dict["role"])
        entity_to_update.set_password(entity_dict["password"])
        entity_to_update.set_lastname(entity_dict["lastname"])
        entity_to_update.set_firstname(entity_dict["firstname"])
        entity_to_update.set_birth_at(entity_dict["birth_at"])

        # Apply changes
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
    Updates the information of an existing user in the database.

    Parameters:
        entity_dict (dict): A dictionary containing the information to be updated.
        email (str): The email of the user to be updated.

    Returns:
        dict: The updated user information, excluding the password.

    Raises:
        UserNotFoundError: If the user is not found.
    """
    db: Session = next(get_db())
    try:
        entity_to_update: Entity = db.query(Entity).filter(
            Entity._email == email).first()
        if entity_to_update is None:
            raise UserNotFoundError()

        # Update fields if provided
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

        # Apply changes
        entity_update_dict: dict = entity_to_update.to_dict()
        db.add(entity_to_update)
        db.commit()
        del entity_update_dict["password"]
        return entity_update_dict

    except UserNotFoundError:
        raise
    finally:
        db.close()


def check_email(entity_dict: dict) -> bool:
    """
    Finds a user in the database based on their email.

    Parameters:
        entity_dict (dict): A dictionary containing the email of the user to search for.

    Returns:
        dict: The user's information, excluding the password.

    Raises:
        UserNotFoundError: If the user is not found.
    """
    db: Session = next(get_db())
    try:
        entity = db.query(Entity).filter(
            Entity._email == entity_dict["email"]).first()
        if not entity:
            return False
        return True
    except:
        db.rollback()
        raise
