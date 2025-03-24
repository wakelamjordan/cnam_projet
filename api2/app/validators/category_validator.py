from app.errors.category_error import CategoryNotValid


def category_insert_dict(category_dict: dict):
    """
    Valide un dictionnaire de catégorie pour l'insertion.

    Cette fonction vérifie que le dictionnaire fourni est bien un dictionnaire et qu'il contient
    la clé 'name'. Si l'une de ces conditions n'est pas remplie, une exception CategoryNotValid
    est levée.

    Args:
        category_dict (dict): Le dictionnaire représentant la catégorie à insérer.

    Raises:
        CategoryNotValid: Si le dictionnaire n'est pas valide ou si la clé 'name' est manquante.
    """
    try:
        if not isinstance(category_dict, dict):
            raise CategoryNotValid("Data type not valid.")
        if "name" not in category_dict:
            raise CategoryNotValid("Data format not valid")
    except CategoryNotValid:
        raise


def category_put_dict(category_dict: dict):
    """
    Valide un dictionnaire de catégorie pour la mise à jour.

    Cette fonction vérifie que le dictionnaire fourni est bien un dictionnaire et qu'il contient
    les clés 'name', 'no', 'parent', 'role', et 'url'. Si l'une de ces conditions n'est pas remplie,
    une exception CategoryNotValid est levée.

    Args:
        category_dict (dict): Le dictionnaire représentant la catégorie à mettre à jour.

    Raises:
        CategoryNotValid: Si le dictionnaire n'est pas valide ou si l'une des clés requises est manquante.
    """
    try:
        category_insert_dict(category_dict)

        if "no" not in category_dict or "parent" not in category_dict or "role" not in category_dict or "url" not in category_dict:
            raise CategoryNotValid("Data format not valid")
    except CategoryNotValid:
        raise
