import re
from urllib.parse import urlparse


class InvalidUrlError(ValueError):
    pass


def _input_host(url: str) -> str:
    trimmed = url.strip()
    without_scheme = re.sub(r"^https?://", "", trimmed, flags=re.IGNORECASE)
    return without_scheme.split("/")[0].split("?")[0].split("#")[0].split(":")[0]


def validate_url(url: str) -> str:
    """Проверяет URL; возвращает trimmed. Бросает InvalidUrlError."""
    trimmed = url.strip()
    if not trimmed:
        raise InvalidUrlError("URL is required")

    host = _input_host(trimmed)
    if re.fullmatch(r"\d+", host):
        raise InvalidUrlError("Invalid URL: enter a domain (e.g. example.com)")

    candidate = trimmed if re.match(r"^https?://", trimmed, re.IGNORECASE) else f"https://{trimmed}"
    parsed = urlparse(candidate)

    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise InvalidUrlError("Invalid URL")

    hostname = parsed.hostname
    if hostname == "localhost":
        return trimmed

    if re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}", hostname):
        return trimmed

    if not re.search(r"[a-zA-Z]", hostname) or "." not in hostname:
        raise InvalidUrlError("Invalid URL")

    tld = hostname.rsplit(".", 1)[-1]
    if len(tld) < 2 or not re.fullmatch(r"[a-zA-Z]{2,}", tld):
        raise InvalidUrlError("Invalid URL")

    return trimmed


def build_redirect_url(url: str) -> str:
    if "http" in url:
        return url
    return f"https://{url}"
