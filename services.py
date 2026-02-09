import secrets
import string


def generate_short_code(length: int = 6) -> str:
    """Генерация уникального короткого кода."""
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))
