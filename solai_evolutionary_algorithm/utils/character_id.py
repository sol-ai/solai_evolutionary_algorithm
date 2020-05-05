import uuid


def create_character_id() -> str:
    return str(uuid.uuid4())
