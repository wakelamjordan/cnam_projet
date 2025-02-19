from ..models import get_db
from ..models.user_model import User as Entity
from sqlalchemy.orm import Session


def insert(entity: Entity):
    with next(get_db()) as db:
        db: Session = next(get_db())
        db.add(entity)
        db.flush()
        db.commit()
    return


def delete(email: str):
    entity_find = find_by_email(email)
    with next(get_db()) as db:
        if not entity_find:
            return None
        db.delete(entity_find)
        db.commit()
        return email


def find_by_email(email: str):
    with next(get_db()) as db:
        return db.query(Entity).filter(Entity.email == email).first()
