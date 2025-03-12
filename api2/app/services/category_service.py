from app.models import get_db
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from app.models.category_model import Category
from app.models.role_model import Role
from app.errors.category_error import CategoryNotValid, CategoryAlreadyExist, CategoryNotExist, CategoryHavePublication, CategoryHaveSub
from app.errors.role_error import RoleNotFoundError
from app.validators.category_validator import category_insert_dict as validator_category_insert_dict, category_put_dict as validator_category_put_dict


def find_all(role_auth: str = None):
    """
    Récupère toutes les catégories en fonction du rôle d'autorisation.

    Cette fonction filtre les catégories selon le rôle d'autorisation fourni.
    Si aucun rôle n'est fourni, elle retourne les catégories sans rôle.
    Si le rôle est 'ROLE_USER', elle retourne les catégories sans rôle ou avec le rôle 'ROLE_USER'.
    Si le rôle est 'ROLE_ADMIN', elle retourne toutes les catégories.

    Args:
        role_auth (str, optional): Le rôle d'autorisation de l'utilisateur. Par défaut None.

    Returns:
        List[dict]: Liste des catégories sous forme de dictionnaires.
    """
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
    """
    Insère une nouvelle catégorie dans la base de données.

    Cette fonction valide le dictionnaire de catégorie, vérifie l'unicité du nom et de l'URL,
    puis insère la nouvelle catégorie dans la base de données.

    Args:
        category_dict (dict): Dictionnaire contenant les données de la nouvelle catégorie.

    Returns:
        str: Le nom de la catégorie insérée.

    Raises:
        CategoryAlreadyExist: Si le nom ou l'URL de la catégorie existe déjà.
        CategoryNotExist: Si la catégorie parente ou le rôle spécifié n'existe pas.
        RoleNotFoundError: Si le rôle spécifié n'existe pas.
    """
    db: Session = next(get_db())
    try:
        validator_category_insert_dict(category_dict)
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
    """
    Supprime une catégorie de la base de données.

    Cette fonction vérifie si la catégorie existe, puis la supprime si elle n'a pas de publications
    ou de sous-catégories associées.

    Args:
        category_dict (dict): Dictionnaire contenant le nom de la catégorie à supprimer.

    Returns:
        str: Le nom de la catégorie supprimée.

    Raises:
        CategoryNotExist: Si la catégorie n'existe pas.
        CategoryHavePublication: Si la catégorie a des publications associées.
        CategoryHaveSub: Si la catégorie a des sous-catégories.
    """
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


def put(category_dict: dict):
    """
    Met à jour une catégorie existante dans la base de données.

    Cette fonction valide les données de mise à jour, vérifie l'unicité du nom et de l'URL,
    puis met à jour la catégorie existante.

    Args:
        category_dict (dict): Dictionnaire contenant le nom de la catégorie à mettre à jour et les nouvelles données.

    Returns:
        str: Le nom de la catégorie mise à jour.

    Raises:
        CategoryNotValid: Si les données de la catégorie ne sont pas valides.
        CategoryNotExist: Si la catégorie ou la catégorie parente n'existe pas.
        RoleNotFoundError: Si le rôle spécifié n'existe pas.
    """
    db: Session = next(get_db())
    try:
        category_to_put: Category = db.query(Category).filter(
            Category._name == category_dict["category"]).first()

        if not category_to_put:
            raise CategoryNotExist()

        data_to_put: dict = category_dict["data"]

        validator_category_put_dict(data_to_put)

        if data_to_put["name"] != category_to_put.get_name(
        ) or data_to_put["url"] != category_to_put.get_url(
        ) or data_to_put["parent"] != category_to_put.get_parent(
        ) or data_to_put["role"] != category_to_put.get_role():
            test_dispo_name_url = db.query(Category).filter(
                or_(Category._name == data_to_put["name"],
                    Category._url == data_to_put["url"]),
                and_(Category._name != category_to_put.get_name())).all()
            if test_dispo_name_url:
                raise CategoryNotValid(
                    'The name or the url is not disponible.')
            if data_to_put['parent'] and not db.query(Category).filter(
                    Category._name == data_to_put['parent']).first():
                raise CategoryNotExist('Parent does not exist!')

            if data_to_put['role'] and not db.query(Role).filter(
                    Role._name == data_to_put['role']).first():
                raise RoleNotFoundError()

        properties_to_maj: list = ['name', 'no', 'parent', 'role', 'url']
        for property in properties_to_maj:
            set_method_name: str = f'set_{property}'
            method = getattr(category_to_put, set_method_name)
            method(data_to_put[property])
        db.add(category_to_put)
        db.commit()
        return category_to_put.get_name()
    except CategoryNotValid:
        db.rollback()
        raise
    except CategoryNotExist:
        db.rollback()
        raise
    except RoleNotFoundError:
        db.rollback()
        raise
    finally:
        db.close()
