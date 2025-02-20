from ..models import get_db
from ..models.user_model import User as Entity
from sqlalchemy.orm import Session
from ..errors.user_error import UserNotFoundError, UserEmailDoesExist


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
    try:
        db.add(entity)
        db.commit()
        return entity.get_email()
    except Exception:
        db.rollback()
        raise UserEmailDoesExist({'error': 'Email already exists!'})
    finally:
        db.close()


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
        raise
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
            raise UserNotFoundError({'error': 'User not found!'})
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
    db: Session = next(get_db())
    try:
        db.merge(entity)
        db.commit()
        return find_by_email(entity)
    finally:
        db.close()
