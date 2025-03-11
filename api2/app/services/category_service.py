from app.models import get_db
from sqlalchemy.orm import Session
from app.models.category_model import Category
from app.errors.category_error import CategoryAlreadyExist


def find_all(role_auth: str = None):
    # faudra gérer le role pour afficher les bons roles mais il me manque des catégory admin
    db: Session = next(get_db())
    try:
        categories: list = db.query(Category).all()
        for x in range(len(categories)):
            categories[x] = categories[x].to_dict()
        return categories
    finally:
        db.close()


def insert(category: dict):
    # faudra gérer le role pour afficher les bons roles mais il me manque des catégory admin
    db: Session = next(get_db())
    try:
        name_x_url_used = db.query(Category).filter(
            Category._name == category['name']).first()
        if name_x_url_used:
            raise CategoryAlreadyExist()
    except CategoryAlreadyExist:
        db.rollback()
    finally:
        db.close()
