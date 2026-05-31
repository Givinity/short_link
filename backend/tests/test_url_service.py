import pytest

from services.url import InvalidUrlError, build_redirect_url, validate_url


class TestBuildRedirectUrl:
    def test_keeps_url_with_http(self):
        assert build_redirect_url("https://google.com") == "https://google.com"

    def test_adds_https_when_missing(self):
        assert build_redirect_url("google.com") == "https://google.com"


class TestValidateUrl:
    def test_accepts_domain_with_scheme(self):
        assert validate_url("https://google.com") == "https://google.com"

    def test_accepts_domain_without_scheme(self):
        assert validate_url("google.com") == "google.com"

    def test_accepts_localhost(self):
        assert validate_url("http://localhost:8000/docs") == "http://localhost:8000/docs"

    def test_rejects_bare_number(self):
        with pytest.raises(InvalidUrlError):
            validate_url("123")

    def test_rejects_empty(self):
        with pytest.raises(InvalidUrlError):
            validate_url("   ")

    def test_rejects_garbage(self):
        with pytest.raises(InvalidUrlError):
            validate_url("not a url")
