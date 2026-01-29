import random
import string

def generate_password(length: int = 12) -> str:
    """
    Generate a strong random password
    """
    if length < 6:
        raise ValueError("Password length must be at least 6")

    characters = (
        string.ascii_lowercase +
        string.ascii_uppercase +
        string.digits +
        string.punctuation
    )

    return "".join(random.choice(characters) for _ in range(length))