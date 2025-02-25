from app.models import get_db
from app.models.user_model import User as Entity
from sqlalchemy.orm import Session
from app.errors.user_error import UserNotFoundError, UserEmailDoesExist
from sqlalchemy.exc import IntegrityError


def insert(entity: Entity) -> str:
    """
    Insère un nouvel utilisateur dans la base de données.

    Paramètre:
        entity (Entity) : L'utilisateur à insérer.
    
    Retourne:
        str : L'email de l'utilisateur inséré.

    Lève:
        UserEmailDoesExist : Si l'email existe déjà.
    """
    db: Session = next(get_db())
    email: str = entity.get_email()

    try:
        check_email = db.query(Entity).filter(
            Entity._email == entity.get_email()).first()
        if check_email != None:
            raise UserEmailDoesExist()
        db.add(entity)
        db.commit()

    except UserEmailDoesExist:
        db.rollback()
        raise
    finally:
        db.close()

    return email
    # try:
    #     # Vérifier si un utilisateur avec cet email existe déjà
    #     # existing_user = find_by_email(entity)
    #     existing_user = db.query(Entity).filter(
    #         Entity._email == entity.get_email()).first()
    #     print(existing_user)

    #     if existing_user:
    #         raise UserEmailDoesExist(
    #             f"L'email {entity.get_email()} existe déjà.")
    #     db.add(entity)
    #     db.commit()
    #     return entity.get_email()
    # except IntegrityError:
    #     db.rollback()
    #     raise UserEmailDoesExist(
    #         f"L'email {entity.get_email()} existe déjà (contrainte UNIQUE).")
    # finally:
    #     db.close()


def delete(entity: Entity) -> str:
    """
    Supprime un utilisateur par email.

    Paramètre:
        entity (Entity) : L'utilisateur à supprimer.
    
    Retourne:
        str : L'email de l'utilisateur supprimé.
    
    Lève:
        UserNotFoundError : Si l'utilisateur n'existe pas.
    """
    db: Session = next(get_db())
    try:
        entity_find = find_by_email(entity)
        db.delete(entity_find)
        db.commit()
        return entity.get_email()
    except UserNotFoundError:
        db.rollback()
        raise UserNotFoundError()
    finally:
        db.close()


def find_by_email(entity: Entity) -> Entity:
    """
    Recherche un utilisateur par email.

    Paramètre:
        entity (Entity) : L'utilisateur avec l'email à rechercher.
    
    Retourne:
        Entity : L'utilisateur trouvé.
    
    Lève:
        UserNotFoundError : Si aucun utilisateur n'est trouvé.
    """
    db: Session = next(get_db())
    try:
        result = db.query(Entity).filter(
            Entity._email == entity.get_email()).first()
        if not result:
            raise UserNotFoundError
        return result
    finally:
        db.close()


def find_all() -> list:
    """
    Récupère tous les utilisateurs.

    Retourne:
        list : Liste des utilisateurs.
    """
    db: Session = next(get_db())
    try:
        return db.query(Entity).all()
    finally:
        db.close()


def update(entity: Entity) -> Entity:
    """
    Met à jour un utilisateur.

    Paramètre:
        entity (Entity) : L'utilisateur à mettre à jour.
    
    Retourne:
        Entity : L'utilisateur mis à jour.
    """
    # Vérifie si le mot de passe est défini, sinon ne le change pas
    db: Session = next(get_db())
    if entity.get_password() is None:
        entity.set_password(find_by_email(entity).get_password()
                            )  # Garde l'ancien mot de passe si non spécifié
    try:

        db.merge(entity)
        db.commit()
        return find_by_email(entity)
    except UserNotFoundError:
        raise UserNotFoundError
    finally:
        db.close()
