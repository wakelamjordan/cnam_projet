from app.errors.category_error import CategoryNotValid


def category_insert_dict(category_dict: dict):
    try:
        if not type(category_dict) == dict:
            raise CategoryNotValid("Data type not valid.")
        if not "name" in category_dict:
            raise CategoryNotValid("Data format not valid")
    except CategoryNotValid:
        raise


def category_put_dict(category_dict: dict):
    try:
        category_insert_dict(category_dict)

        if not "no" in category_dict or not "parent" in category_dict or not "role" in category_dict or not "url" in category_dict:
            raise CategoryNotValid("Data format not valid")
    except CategoryNotValid:
        raise
