import hashlib
import string

_ALPHABET = string.ascii_letters + string.digits
_BASE = len(_ALPHABET)


def generate_short_code_from_url(
    url: str,
    length: int = 6,
    attempt: int = 0,
) -> str:
    """Детерминированный код из URL; attempt > 0 — при коллизии с другим URL."""
    payload = f"{url}:{attempt}" if attempt else url
    digest = hashlib.sha256(payload.encode()).digest()
    num = int.from_bytes(digest[:8], "big")
    chars: list[str] = []
    for _ in range(length):
        chars.append(_ALPHABET[num % _BASE])
        num //= _BASE
    return "".join(reversed(chars))
