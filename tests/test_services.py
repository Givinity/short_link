import string

from services import generate_short_code


class TestGenerateShortCode:
    """Тесты для функции генерации короткого кода."""

    def test_default_length(self):
        """Проверка длины по умолчанию (6 символов)."""
        code = generate_short_code()
        assert len(code) == 6

    def test_custom_length(self):
        """Проверка кастомной длины."""
        code = generate_short_code(length=10)
        assert len(code) == 10

    def test_contains_only_alphanumeric(self):
        """Проверка что код содержит только буквы и цифры."""
        code = generate_short_code()
        allowed = string.ascii_letters + string.digits
        assert all(char in allowed for char in code)

    def test_generates_unique_codes(self):
        """Проверка что генерируются разные коды."""
        codes = {generate_short_code() for _ in range(100)}
        # При 62^6 комбинаций, 100 кодов должны быть уникальными
        assert len(codes) == 100

    def test_zero_length_returns_empty(self):
        """Проверка что length=0 возвращает пустую строку."""
        code = generate_short_code(length=0)
        assert code == ""
