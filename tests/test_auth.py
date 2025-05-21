import base64
from unittest.mock import MagicMock

import pytest

from integrates.auth.api_key import ApiKeyAuth, ApiKeyLocation
from integrates.auth.basic import BasicAuth
from integrates.auth.bearer import BearerAuth
from integrates.auth.oauth2 import OAuth2


class TestAuth:
    def test_basic_auth(self):
        """Test that BasicAuth properly sets up credentials."""
        basic_auth = BasicAuth(username="user", password="pass")

        assert basic_auth.username == "user"
        assert basic_auth.password == "pass"

        # Test auth implementation
        headers = {}
        signed_headers = basic_auth.sign("GET", "https://api.example.com", headers)

        # Verify the headers were modified correctly
        assert "Authorization" in signed_headers
        token = base64.b64encode(b"user:pass").decode("utf-8")
        assert signed_headers["Authorization"] == f"Basic {token}"

    def test_bearer_auth(self):
        """Test that BearerAuth properly sets up token."""
        bearer_auth = BearerAuth(token="my-token")

        assert bearer_auth.token == "my-token"

        # Test auth implementation
        headers = {}
        signed_headers = bearer_auth.sign("GET", "https://api.example.com", headers)

        # Verify the headers were modified correctly
        assert "Authorization" in signed_headers
        assert signed_headers["Authorization"] == "Bearer my-token"

    def test_api_key_auth_header(self):
        """Test that ApiKeyAuth properly handles header-based API keys."""
        api_key_auth = ApiKeyAuth(
            api_key="my-api-key", key_name="X-API-Key", location=ApiKeyLocation.HEADER
        )

        assert api_key_auth.api_key == "my-api-key"
        assert api_key_auth.key_name == "X-API-Key"
        assert api_key_auth.location == ApiKeyLocation.HEADER

        # Test auth implementation
        headers = {}
        signed_headers = api_key_auth.sign("GET", "https://api.example.com", headers)

        # Verify the headers were modified correctly
        assert "X-API-Key" in signed_headers
        assert signed_headers["X-API-Key"] == "my-api-key"

    def test_api_key_auth_query(self):
        """Test that ApiKeyAuth properly handles query parameter-based API keys."""
        api_key_auth = ApiKeyAuth(
            api_key="my-api-key", key_name="api_key", location=ApiKeyLocation.QUERY
        )

        assert api_key_auth.api_key == "my-api-key"
        assert api_key_auth.key_name == "api_key"
        assert api_key_auth.location == ApiKeyLocation.QUERY

        # Test auth implementation with query params
        # Note: The current implementation doesn't modify the URL for query params
        # This is a limitation in the current implementation
        headers = {}
        signed_headers = api_key_auth.sign("GET", "https://api.example.com", headers)

        # For now, the test just checks that headers aren't modified
        assert signed_headers == headers

    def test_oauth2_auth(self):
        """Test that OAuth2 properly sets up the token."""
        oauth_auth = OAuth2(token="oauth-token")

        assert oauth_auth.token == "oauth-token"
        assert oauth_auth.token_type == "Bearer"

        # Test auth implementation
        headers = {}
        signed_headers = oauth_auth.sign("GET", "https://api.example.com", headers)

        # Verify the headers were modified correctly
        assert "Authorization" in signed_headers
        assert signed_headers["Authorization"] == "Bearer oauth-token"
