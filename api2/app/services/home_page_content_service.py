from app.models import get_db
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.home_page_content_model import HomePageContent as Entity
from app.models.publication_model import Publication
from app.errors.service_error import ResultEmpty
from sqlalchemy.exc import IntegrityError


def select_all():
    """
    Récupère toutes les entités de la base de données.

    Returns:
        List[dict]: Une liste de dictionnaires représentant chaque entité.
    """
    db: Session = next(get_db())

    entities: list[Entity] = db.query(Entity).all()

    for x in range(len(entities)):
        entity: Entity = entities[x]
        entities[x] = entity.to_dict()
    db.commit()
    db.close()

    return entities


def insert(data: dict):
    """
    Insère une nouvelle entité dans la base de données.

    Args:
        data (dict): Les données de la nouvelle entité à insérer.

    Returns:
        str: Le nom de l'entité nouvellement insérée.
    """
    db: Session = next(get_db())
    entity: Entity = Entity(data['name'], data['element'], data['description'])
    db.add(entity)
    db.commit()
    db.close()
    return data['name']


def replace(data: dict):
    """
    Remplace une entité existante par de nouvelles données.

    Args:
        data (dict): Les nouvelles données pour remplacer l'entité existante.

    Returns:
        str: Le nom de l'entité mise à jour.

    Raises:
        ResultEmpty: Si l'entité ou la publication n'est pas trouvée.
        IntegrityError: Si une contrainte d'intégrité est violée.
    """
    db: Session = next(get_db())
    try:
        entity: Entity = db.query(Entity).filter(
            Entity._name == data['name']).first()
        if not entity:
            raise ResultEmpty()

        properties: list = ['name', 'element', 'description']

        for property in properties:
            set_method_name: str = f'set_{property}'
            method = getattr(entity, set_method_name)
            method(data['put'][property])

        if 'publication' in data and data['publication']:
            publication: Publication = db.query(Publication).filter(
                Publication._title == data['put']['publication']).first()
            if not publication:
                raise ResultEmpty()
            entity.set_publication(publication.get_title())

        result: str = entity.get_name()
        db.add(entity)
        db.commit()
        return result
    except ResultEmpty:
        db.rollback()
        raise
    except IntegrityError:
        db.rollback()
        raise
    finally:
        db.close()


def update(data: dict):
    """
    Met à jour une entité existante avec de nouvelles données.

    Args:
        data (dict): Les données mises à jour pour l'entité.

    Returns:
        str: Le nom de l'entité mise à jour.

    Raises:
        ResultEmpty: Si l'entité ou la publication n'est pas trouvée.
        IntegrityError: Si une contrainte d'intégrité est violée.
    """
    db: Session = next(get_db())
    try:
        entity: Entity = db.query(Entity).filter(
            Entity._name == data['name']).first()
        if not entity:
            raise ResultEmpty()

        if 'publication' in data and data['publication']:
            publication: Publication = db.query(Publication).filter(
                Publication._title == data['publication']).first()
            if not publication:
                raise ResultEmpty()
            entity.set_publication(publication.get_title())

        result: str = entity.get_name()
        db.add(entity)
        db.commit()
        return result
    except ResultEmpty:
        db.rollback()
        raise
    except IntegrityError:
        db.rollback()
        raise
    finally:
        db.close()


def select_one(entity: dict):
    """
    Récupère une entité spécifique de la base de données.

    Args:
        entity (dict): Les données de l'entité à récupérer.

    Returns:
        dict: Un dictionnaire représentant l'entité.

    Raises:
        ResultEmpty: Si l'entité n'est pas trouvée.
    """
    db: Session = next(get_db())
    try:
        entity: Entity = db.query(Entity).filter(
            Entity._name == entity['name']).first()
        if not entity:
            raise ResultEmpty()
        response: dict = entity.to_dict()
        db.commit()
        return response
    except ResultEmpty:
        db.rollback()
        raise
    finally:
        db.close()


def delete(entity: dict):
    """
    Supprime une entité de la base de données.

    Args:
        entity (dict): Les données de l'entité à supprimer.

    Returns:
        str: Le nom de l'entité supprimée.

    Raises:
        ResultEmpty: Si l'entité n'est pas trouvée.
    """
    db: Session = next(get_db())
    try:
        entity: Entity = db.query(Entity).filter(
            Entity._name == entity['name']).first()
        if not entity:
            raise ResultEmpty()
        response: dict = entity.to_dict()
        db.delete(entity)
        db.commit()
        return response['name']
    except ResultEmpty:
        db.rollback()
        raise
    finally:
        db.close()


def disponibility_insert(data: dict) -> bool:
    """
    Vérifie la disponibilité d'une entité pour l'insertion.

    Args:
        data (dict): Les données de l'entité à vérifier.

    Returns:
        bool: True si l'entité peut être insérée, False sinon.
    """
    db: Session = next(get_db())

    search: Entity = db.query(Entity).filter(
        or_(Entity._name == data['name'],
            Entity._element == data['element'])).all()
    db.commit()
    db.close()
    return bool(not search)
