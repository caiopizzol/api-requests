import datetime
from unittest.mock import MagicMock, patch

import httpx
import pytest

from integrates.core.client import Client


class TestClient:
    def test_init_default(self):
        """Test that a client can be initialized with default parameters."""
        client = Client()
        assert client is not None
        assert client.base_url == ""
        assert isinstance(client.timeout, httpx.Timeout)

    def test_init_with_params(self):
        """Test that a client can be initialized with custom parameters."""
        client = Client(
            base_url="https://api.example.com", timeout=30.0, headers={"X-Custom-Header": "value"}
        )
        assert client.base_url == "https://api.example.com"
        assert client.timeout.connect == 30.0
        # headers are passed to the httpx client, not stored on the client object

    @patch("httpx.Client.request")
    def test_get_request(self, mock_request, mock_response):
        """Test that GET requests are properly formatted."""
        response = httpx.Response(
            status_code=200,
            content=b'{"key": "value"}',
            request=httpx.Request("GET", "https://api.example.com/endpoint"),
        )
        # Set the elapsed attribute so Response.from_httpx works
        response._elapsed = datetime.timedelta(seconds=0.1)
        mock_request.return_value = response

        client = Client()
        response = client.get("https://api.example.com/endpoint")

        mock_request.assert_called_once()
        assert mock_request.call_args[1]["method"] == "GET"
        assert mock_request.call_args[1]["url"] == "https://api.example.com/endpoint"

    @patch("httpx.Client.request")
    def test_post_request_with_json(self, mock_request, mock_response):
        """Test that POST requests with JSON data are properly formatted."""
        response = httpx.Response(
            status_code=201,
            content=b"",
            request=httpx.Request("POST", "https://api.example.com/endpoint"),
        )
        response._elapsed = datetime.timedelta(seconds=0.1)
        mock_request.return_value = response

        client = Client()
        data = {"name": "test", "value": 123}
        client.post("https://api.example.com/endpoint", json=data)

        mock_request.assert_called_once()
        assert mock_request.call_args[1]["method"] == "POST"
        assert mock_request.call_args[1]["json"] == data

    @patch("httpx.Client.request")
    def test_request_with_params(self, mock_request, mock_response):
        """Test that requests with query parameters are properly formatted."""
        response = httpx.Response(
            status_code=200,
            content=b"",
            request=httpx.Request("GET", "https://api.example.com/endpoint"),
        )
        response._elapsed = datetime.timedelta(seconds=0.1)
        mock_request.return_value = response

        client = Client()
        params = {"page": 1, "limit": 10}
        client.get("https://api.example.com/endpoint", params=params)

        mock_request.assert_called_once()
        assert mock_request.call_args[1]["params"] == params

    @patch("httpx.Client.request")
    def test_request_with_auth(self, mock_request, mock_response):
        """Test that requests with authentication are properly handled."""
        response = httpx.Response(
            status_code=200,
            content=b"",
            request=httpx.Request("GET", "https://api.example.com/endpoint"),
        )
        response._elapsed = datetime.timedelta(seconds=0.1)
        mock_request.return_value = response

        # Create a mock Auth object
        mock_auth = MagicMock()
        mock_auth.sign.return_value = {"Authorization": "Bearer token"}

        client = Client(auth=mock_auth)
        client.get("https://api.example.com/endpoint")

        # Verify auth.sign was called
        mock_auth.sign.assert_called_once()

    @patch("httpx.Client.request")
    def test_request_error_handling(self, mock_request, mock_response):
        """Test that HTTP errors are properly handled."""
        response = httpx.Response(
            status_code=404,
            content=b"Not Found",
            request=httpx.Request("GET", "https://api.example.com/notfound"),
        )
        response._elapsed = datetime.timedelta(seconds=0.1)
        mock_request.return_value = response

        client = Client()
        response = client.get("https://api.example.com/notfound")

        assert response.status_code == 404

    def test_client_context_manager(self):
        """Test that the client can be used as a context manager."""
        with patch("httpx.Client.close") as mock_close:
            with Client() as client:
                assert client is not None

            # Verify client.close() was called
            mock_close.assert_called_once()
