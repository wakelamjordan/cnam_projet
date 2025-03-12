from app.models import get_db
from app.models.role_model import Role as Entity
from sqlalchemy.orm import Session


def select_all() -> list[Entity]:
    db: Session = next(get_db())
    try:
        roles: list[Entity] = []
        for role in db.query(Entity).all():
            roles.append(role.to_dict())
        db.commit()
        return roles
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")
    finally:
        db.close()
