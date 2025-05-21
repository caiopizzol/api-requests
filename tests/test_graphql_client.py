import pytest
from unittest.mock import patch, MagicMock
from integrates.protocols.graphql.client import GraphQLClient


class TestGraphQLClient:
    def test_init(self):
        """Test that GraphQLClient is initialized correctly."""
        client = GraphQLClient(endpoint="https://api.example.com/graphql")

        assert client.base_url == "https://api.example.com/graphql"

    @patch("integrates.core.client.Client.post")
    def test_query(self, mock_post, mock_response):
        """Test that query() method correctly formats GraphQL queries."""
        mock_post.return_value = mock_response(
            status_code=200,
            headers={},
            content=b'{"data": {"user": {"id": "123", "name": "Test User"}}}',
            url="https://api.example.com/graphql",
        )

        client = GraphQLClient(endpoint="https://api.example.com/graphql")
        query = """
        query GetUser($id: ID!) {
            user(id: $id) {
                id
                name
            }
        }
        """
        variables = {"id": "123"}

        response = client.query(query, variables)

        mock_post.assert_called_once()
        assert mock_post.call_args[0][0] == ""  # The endpoint is already in base_url
        assert mock_post.call_args[1]["json"]["query"] == query
        assert mock_post.call_args[1]["json"]["variables"] == variables

    @patch("integrates.core.client.Client.post")
    def test_mutation(self, mock_post, mock_response):
        """Test that mutation() method correctly formats GraphQL mutations."""
        mock_post.return_value = mock_response(
            status_code=200,
            headers={},
            content=b'{"data": {"createUser": {"id": "456", "name": "New User"}}}',
            url="https://api.example.com/graphql",
        )

        client = GraphQLClient(endpoint="https://api.example.com/graphql")
        mutation = """
        mutation CreateUser($input: UserInput!) {
            createUser(input: $input) {
                id
                name
            }
        }
        """
        variables = {"input": {"name": "New User", "email": "user@example.com"}}

        response = client.mutation(mutation, variables)

        mock_post.assert_called_once()
        assert mock_post.call_args[0][0] == ""  # The endpoint is already in base_url
        assert mock_post.call_args[1]["json"]["query"] == mutation
        assert mock_post.call_args[1]["json"]["variables"] == variables

    @patch("integrates.core.client.Client.post")
    def test_query_with_invalid_response(self, mock_post, mock_response):
        """Test that GraphQLClient handles error responses correctly."""
        mock_post.return_value = mock_response(
            status_code=200,
            headers={},
            content=b'{"errors": [{"message": "Field \'users\' doesn\'t exist", "locations": [{"line": 2, "column": 9}]}]}',
            url="https://api.example.com/graphql",
        )

        client = GraphQLClient(endpoint="https://api.example.com/graphql")
        query = """
        query {
            users {
                id
                name
            }
        }
        """

        response = client.query(query)
        data = response.json()

        assert "errors" in data
        assert len(data["errors"]) == 1

    @patch("integrates.core.client.Client.post")
    def test_query_with_operation_name(self, mock_post, mock_response):
        """Test that operationName is correctly included when provided."""
        mock_post.return_value = mock_response(
            status_code=200,
            headers={},
            content=b'{"data": {"user": {"id": "123", "name": "Test User"}}}',
            url="https://api.example.com/graphql",
        )

        client = GraphQLClient(endpoint="https://api.example.com/graphql")
        query = """
        query GetUser($id: ID!) {
            user(id: $id) {
                id
                name
            }
        }
        """
        variables = {"id": "123"}
        operation_name = "GetUser"

        response = client.query(query, variables, operation_name)

        mock_post.assert_called_once()
        assert mock_post.call_args[1]["json"]["operationName"] == operation_name
