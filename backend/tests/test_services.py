import string

from services.short_link import generate_short_code_from_url


class TestGenerateShortCodeFromUrl:
    def test_default_length(self):
        code = generate_short_code_from_url("https://google.com")
        assert len(code) == 6

    def test_custom_length(self):
        code = generate_short_code_from_url("https://google.com", length=10)
        assert len(code) == 10

    def test_contains_only_alphanumeric(self):
        code = generate_short_code_from_url("https://google.com")
        allowed = string.ascii_letters + string.digits
        assert all(char in allowed for char in code)

    def test_same_url_produces_same_code(self):
        url = "https://google.com"
        assert generate_short_code_from_url(url) == generate_short_code_from_url(url)

    def test_different_urls_produce_different_codes(self):
        code_a = generate_short_code_from_url("https://google.com")
        code_b = generate_short_code_from_url("https://example.com")
        assert code_a != code_b

    def test_attempt_changes_code(self):
        url = "https://google.com"
        base = generate_short_code_from_url(url, attempt=0)
        retry = generate_short_code_from_url(url, attempt=1)
        assert base != retry
