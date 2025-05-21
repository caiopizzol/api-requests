"""
Authentication examples using Integrates.

This example demonstrates how to use different authentication methods with Integrates.
"""

import os

import integrates as api
from integrates.auth import ApiKeyAuth, BasicAuth, BearerAuth, OAuth2
from integrates.auth.api_key import ApiKeyLocation


def basic_auth_example():
    """Example using Basic authentication."""
    # Create a client with Basic authentication
    client = api.Client(auth=BasicAuth(username="user", password="pass"))

    # The auth headers will be automatically added to all requests
    response = client.get("https://httpbin.org/basic-auth/user/pass")
    print(f"Basic Auth Status: {response.status_code}")
    print(f"Response: {response.json()}")


def bearer_auth_example():
    """Example using Bearer token authentication."""
    # In a real app, you would get this token from an OAuth flow or other source
    token = "my-token"

    # Create a client with Bearer authentication
    client = api.Client(auth=BearerAuth(token=token))

    # The Authorization header will be automatically added to all requests
    response = client.get("https://httpbin.org/headers")
    print(f"Bearer Auth Headers: {response.json()}")


def api_key_example():
    """Example using API key authentication."""
    # API key in header (default)
    header_client = api.Client(auth=ApiKeyAuth(api_key="my-api-key", key_name="X-API-Key"))

    # The API key header will be automatically added to all requests
    response = header_client.get("https://httpbin.org/headers")
    print(f"API Key in Header: {response.json()}")

    # API key in query parameter
    query_client = api.Client(
        auth=ApiKeyAuth(api_key="my-api-key", key_name="api_key", location=ApiKeyLocation.QUERY)
    )

    # The API key will be automatically added to the query string
    # Note: Currently this requires manual implementation for query params
    response = query_client.get("https://httpbin.org/get", params={"api_key": "my-api-key"})
    print(f"API Key in Query: {response.json()}")


if __name__ == "__main__":
    print("Basic Authentication Example:")
    basic_auth_example()

    print("\nBearer Authentication Example:")
    bearer_auth_example()

    print("\nAPI Key Authentication Example:")
    api_key_example()
