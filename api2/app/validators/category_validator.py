from app.errors.category_error import CategoryNotValid


def category_dict(category_dict: dict):
    try:
        if not type(category_dict) == dict:
            raise CategoryNotValid("Data type not valid.")
        if not "name" in category_dict:
            raise CategoryNotValid("Data format not valid")
    except CategoryNotValid:
        raise
