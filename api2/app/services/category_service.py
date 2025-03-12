from app.models import get_db
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.category_model import Category
from app.models.role_model import Role
from app.errors.category_error import CategoryAlreadyExist, CategoryNotExist, CategoryHavePublication, CategoryHaveSub
from app.errors.role_error import RoleNotFoundError
from app.validators.category_validator import category_dict as validator_category_dict


def find_all(role_auth: str = None):
    db: Session = next(get_db())
    try:
        match role_auth:
            case None:
                categories = db.query(Category).filter(
                    Category.role == None).all()
            case 'ROLE_USER':
                categories = db.query(Category).filter(
                    or_(Category.role == None,
                        Category.role.has(Role._name == 'ROLE_USER'))).all()
            case 'ROLE_ADMIN':
                categories = db.query(Category).all()
        for x in range(len(categories)):
            category_dict = categories[x].to_dict()
            categories[x] = category_dict
        return categories
    finally:
        db.close()


def insert(category_dict: dict):
    db: Session = next(get_db())
    try:
        validator_category_dict(category_dict)
        name_x_url_used = db.query(Category).filter(
            Category._name == category_dict['name']).first()
        if name_x_url_used:
            raise CategoryAlreadyExist()
        category: Category = Category(name=category_dict['name'])

        if 'url' in category_dict:
            if db.query(Category).filter(
                    Category._url == category_dict['url']).first():
                raise CategoryAlreadyExist('Url already exist!')
            category.set_url(category_dict['url'])

        if 'no' in category_dict:
            category.set_no(category_dict['no'])

        if 'parent' in category_dict:
            if not db.query(Category).filter(
                    Category._name == category_dict['parent']).first():
                raise CategoryNotExist()
            category.set_parent(category_dict['parent'])

        if 'role' in category_dict:
            if not db.query(Role).filter(
                    Role._name == category_dict['role']).first():
                raise RoleNotFoundError()
            category.set_role(category_dict['role'])

        db.add(category)
        db.commit()
        return category.get_name()
    except CategoryAlreadyExist:
        db.rollback()
        raise
    except CategoryNotExist:
        db.rollback()
        raise
    finally:
        db.close()


def delete(category_dict: dict):
    db = next(get_db())
    try:
        category: Category = db.query(Category).filter(
            Category._name == category_dict['name']).first()
        if not category:
            raise CategoryNotExist()

        if category.publications:
            raise CategoryHavePublication()

        if category.children:
            raise CategoryHaveSub()

        db.delete(category)
        db.commit()
        return category.get_name()
    except CategoryNotExist:
        db.rollback()
        raise
    except CategoryHavePublication:
        db.rollback()
        raise
    except CategoryHaveSub:
        db.rollback()
        raise
    finally:
        db.close()
