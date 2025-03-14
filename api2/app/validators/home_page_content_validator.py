def insert(entity: dict) -> bool:
    data_to_check: list = ["name", "element", "description"]

    for data in data_to_check:
        if not data in entity:
            return False
    return True
