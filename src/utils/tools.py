
import re
import uuid


def mention_to_id(mention: str) -> int:
    return int(re.sub(r'[<>!@]', '', mention))


def generate_uuid() -> str:
    return uuid.uuid4().hex
