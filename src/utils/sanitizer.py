
import re


def mention_to_id(mention: str) -> int:
    return int(re.sub(r'[<>!@]', '', mention))
