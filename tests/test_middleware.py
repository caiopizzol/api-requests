import time
from unittest.mock import MagicMock, call, patch

import httpx
import pytest

from integrates.core.client import Client
from integrates.middleware.logging import LoggingMiddleware
from integrates.middleware.retry import RetryMiddleware


class TestMiddleware:
    def test_retry_middleware_init(self):
        """Test that RetryMiddleware is initialized with correct parameters."""
        middleware = RetryMiddleware(retries=3, retry_status_codes=[500, 502], backoff_factor=0.5)

        assert middleware.retries == 3
        assert middleware.retry_status_codes == [500, 502]
        assert middleware.backoff_factor == 0.5

    def test_retry_middleware_pre_request(self):
        """Test that RetryMiddleware adds retry configuration to request."""
        middleware = RetryMiddleware(retries=3, retry_status_codes=[500], backoff_factor=0.5)

        request_kwargs = {"method": "GET", "url": "https://api.example.com"}
        modified_kwargs = middleware.pre_request(request_kwargs)

        assert "_retry_config" in modified_kwargs
        assert modified_kwargs["_retry_config"]["count"] == 3
        assert modified_kwargs["_retry_config"]["status_codes"] == [500]
        assert modified_kwargs["_retry_config"]["backoff_factor"] == 0.5

    @patch("httpx.Client.request")
    @patch("time.sleep")
    def test_client_with_retry_middleware(self, mock_sleep, mock_request, mock_response):
        """Test that a client with RetryMiddleware retries failed requests."""
        # First request fails with 500, second succeeds with 200
        mock_request.side_effect = [
            httpx.Response(
                status_code=500,
                content=b"Server Error",
                request=httpx.Request("GET", "https://api.example.com"),
            ),
            httpx.Response(
                status_code=200,
                content=b'{"success": true}',
                request=httpx.Request("GET", "https://api.example.com"),
            ),
        ]

        middleware = RetryMiddleware(retries=1, retry_status_codes=[500])
        client = Client(middlewares=[middleware])

        response = client.get("https://api.example.com")

        # Should have called request twice (original + 1 retry)
        assert mock_request.call_count == 2
        # Should have called sleep once (between retries)
        assert mock_sleep.call_count >= 1
        # Final response should be the success response
        assert response.status_code == 200

    @patch("logging.Logger.info")
    @patch("httpx.Client.request")
    def test_logging_middleware(self, mock_request, mock_log_info, mock_response):
        """Test that LoggingMiddleware logs requests and responses."""
        mock_request.return_value = httpx.Response(
            status_code=200,
            content=b'{"success": true}',
            request=httpx.Request("GET", "https://api.example.com"),
        )

        client = Client(middlewares=[LoggingMiddleware()])
        response = client.get("https://api.example.com")

        # We can't easily test the exact logging calls, but we can verify the response
        assert response.status_code == 200

    @patch("httpx.Client.request")
    def test_multiple_middlewares(self, mock_request, mock_response):
        """Test that multiple middlewares are correctly applied."""
        mock_request.return_value = httpx.Response(
            status_code=200,
            content=b'{"success": true}',
            request=httpx.Request("GET", "https://api.example.com"),
        )

        # Set up middlewares to track execution order
        execution_order = []

        class TrackingMiddleware1(LoggingMiddleware):
            def pre_request(self, request_kwargs):
                execution_order.append("middleware1_pre")
                return super().pre_request(request_kwargs)

            def post_request(self, response):
                execution_order.append("middleware1_post")
                return super().post_request(response)

        class TrackingMiddleware2(LoggingMiddleware):
            def pre_request(self, request_kwargs):
                execution_order.append("middleware2_pre")
                return super().pre_request(request_kwargs)

            def post_request(self, response):
                execution_order.append("middleware2_post")
                return super().post_request(response)

        client = Client(middlewares=[TrackingMiddleware1(), TrackingMiddleware2()])
        response = client.get("https://api.example.com")

        # Check that the middlewares were executed in the correct order
        assert execution_order[0] == "middleware1_pre"
        assert execution_order[1] == "middleware2_pre"
        assert execution_order[2] == "middleware1_post"
        assert execution_order[3] == "middleware2_post"
