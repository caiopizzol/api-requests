from unittest.mock import MagicMock, patch

import httpx
import pytest

from integrates.protocols.rest.client import ResourceClient, RestClient


class TestRestClient:
    def test_init(self):
        """Test that RestClient is initialized correctly."""
        client = RestClient(base_url="https://api.example.com")
        assert client.base_url == "https://api.example.com"

    def test_resource_method(self):
        """Test that resource() creates and returns a resource object."""
        client = RestClient(base_url="https://api.example.com")
        resource = client.resource("users")

        assert isinstance(resource, ResourceClient)
        assert resource.path == "users"
        assert resource.client == client

    @patch("integrates.core.client.Client.request")
    def test_resource_get(self, mock_request, mock_response):
        """Test that a resource GET request is properly formatted."""
        mock_request.return_value = mock_response(
            status_code=200,
            headers={},
            content=b'{"id": 1, "name": "User"}',
            url="https://api.example.com/users",
        )

        client = RestClient(base_url="https://api.example.com")
        users = client.resource("users")
        response = users.get()

        mock_request.assert_called_once()
        assert mock_request.call_args[0][0] == "GET"
        assert mock_request.call_args[0][1] == "users"

    @patch("integrates.core.client.Client.request")
    def test_resource_item_get(self, mock_request, mock_response):
        """Test that a resource item GET request is properly formatted."""
        mock_request.return_value = mock_response(
            status_code=200,
            headers={},
            content=b'{"id": 1, "name": "User"}',
            url="https://api.example.com/users/1",
        )

        client = RestClient(base_url="https://api.example.com")
        user = client.resource("users")("1")
        response = user.get()

        mock_request.assert_called_once()
        assert mock_request.call_args[0][0] == "GET"
        assert mock_request.call_args[0][1] == "users/1"

    @patch("integrates.core.client.Client.request")
    def test_resource_post(self, mock_request, mock_response):
        """Test that a resource POST request is properly formatted."""
        mock_request.return_value = mock_response(
            status_code=201,
            headers={},
            content=b'{"id": 2, "name": "New User"}',
            url="https://api.example.com/users",
        )

        client = RestClient(base_url="https://api.example.com")
        users = client.resource("users")
        data = {"name": "New User"}
        response = users.post(json=data)

        mock_request.assert_called_once()
        assert mock_request.call_args[0][0] == "POST"
        assert mock_request.call_args[0][1] == "users"
        assert mock_request.call_args[1]["json"] == data

    @patch("integrates.core.client.Client.request")
    def test_resource_item_put(self, mock_request, mock_response):
        """Test that a resource item PUT request is properly formatted."""
        mock_request.return_value = mock_response(
            status_code=200,
            headers={},
            content=b'{"id": 1, "name": "Updated User"}',
            url="https://api.example.com/users/1",
        )

        client = RestClient(base_url="https://api.example.com")
        user = client.resource("users")("1")
        data = {"name": "Updated User"}
        response = user.put(json=data)

        mock_request.assert_called_once()
        assert mock_request.call_args[0][0] == "PUT"
        assert mock_request.call_args[0][1] == "users/1"
        assert mock_request.call_args[1]["json"] == data

    @patch("integrates.core.client.Client.request")
    def test_resource_item_delete(self, mock_request, mock_response):
        """Test that a resource item DELETE request is properly formatted."""
        mock_request.return_value = mock_response(
            status_code=204, headers={}, content=b"", url="https://api.example.com/users/1"
        )

        client = RestClient(base_url="https://api.example.com")
        user = client.resource("users")("1")
        response = user.delete()

        mock_request.assert_called_once()
        assert mock_request.call_args[0][0] == "DELETE"
        assert mock_request.call_args[0][1] == "users/1"
        assert response.status_code == 204

    @patch("integrates.core.client.Client.request")
    def test_nested_resources(self, mock_request, mock_response):
        """Test that nested resources are properly handled."""
        mock_request.return_value = mock_response(
            status_code=200,
            headers={},
            content=b'{"id": 1, "title": "Post 1"}',
            url="https://api.example.com/users/1/posts/1",
        )

        client = RestClient(base_url="https://api.example.com")
        post = client.resource("users")("1").resource("posts")("1")
        response = post.get()

        mock_request.assert_called_once()
        assert mock_request.call_args[0][0] == "GET"
        assert mock_request.call_args[0][1] == "users/1/posts/1"
