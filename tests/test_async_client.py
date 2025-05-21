import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import httpx
from integrates.core.client import AsyncClient

pytestmark = pytest.mark.asyncio


class TestAsyncClient:
    async def test_init_default(self):
        """Test that an async client can be initialized with default parameters."""
        client = AsyncClient()
        assert client is not None
        assert client.base_url == ""
        assert isinstance(client.timeout, httpx.Timeout)

    async def test_init_with_params(self):
        """Test that an async client can be initialized with custom parameters."""
        client = AsyncClient(
            base_url="https://api.example.com", timeout=30.0, headers={"X-Custom-Header": "value"}
        )
        assert client.base_url == "https://api.example.com"
        assert client.timeout.connect == 30.0
        # headers are passed to the httpx client, not stored on the client object

    @patch("httpx.AsyncClient.request")
    async def test_get_request(self, mock_request, mock_response):
        """Test that GET requests are properly formatted."""
        mock_request.return_value = httpx.Response(
            status_code=200,
            content=b'{"key": "value"}',
            request=httpx.Request("GET", "https://api.example.com/endpoint"),
        )

        async with AsyncClient() as client:
            response = await client.get("https://api.example.com/endpoint")

        mock_request.assert_called_once()
        assert mock_request.call_args[1]["method"] == "GET"
        assert mock_request.call_args[1]["url"] == "https://api.example.com/endpoint"

    @patch("httpx.AsyncClient.request")
    async def test_post_request_with_json(self, mock_request, mock_response):
        """Test that POST requests with JSON data are properly formatted."""
        mock_request.return_value = httpx.Response(
            status_code=201,
            content=b"",
            request=httpx.Request("POST", "https://api.example.com/endpoint"),
        )

        async with AsyncClient() as client:
            data = {"name": "test", "value": 123}
            await client.post("https://api.example.com/endpoint", json=data)

        mock_request.assert_called_once()
        assert mock_request.call_args[1]["method"] == "POST"
        assert mock_request.call_args[1]["json"] == data

    @patch("httpx.AsyncClient.request")
    async def test_request_with_params(self, mock_request, mock_response):
        """Test that requests with query parameters are properly formatted."""
        mock_request.return_value = httpx.Response(
            status_code=200,
            content=b"",
            request=httpx.Request("GET", "https://api.example.com/endpoint"),
        )

        async with AsyncClient() as client:
            params = {"page": 1, "limit": 10}
            await client.get("https://api.example.com/endpoint", params=params)

        mock_request.assert_called_once()
        assert mock_request.call_args[1]["params"] == params

    @patch("httpx.AsyncClient.request")
    async def test_request_with_auth(self, mock_request, mock_response):
        """Test that requests with authentication are properly handled."""
        mock_request.return_value = httpx.Response(
            status_code=200,
            content=b"",
            request=httpx.Request("GET", "https://api.example.com/endpoint"),
        )

        # Create a mock Auth object
        mock_auth = MagicMock()
        mock_auth.sign.return_value = {"Authorization": "Bearer token"}

        async with AsyncClient(auth=mock_auth) as client:
            await client.get("https://api.example.com/endpoint")

        # Verify auth.sign was called
        mock_auth.sign.assert_called_once()

    @patch("httpx.AsyncClient.request")
    async def test_request_error_handling(self, mock_request, mock_response):
        """Test that HTTP errors are properly handled."""
        mock_request.return_value = httpx.Response(
            status_code=404,
            content=b"Not Found",
            request=httpx.Request("GET", "https://api.example.com/notfound"),
        )

        async with AsyncClient() as client:
            response = await client.get("https://api.example.com/notfound")

        assert response.status_code == 404

    async def test_client_context_manager(self):
        """Test that the async client can be used as a context manager."""
        with patch("httpx.AsyncClient.aclose") as mock_close:
            async with AsyncClient() as client:
                assert client is not None

            # Verify client.close() was called
            mock_close.assert_called_once()
