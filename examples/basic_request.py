"""
Basic HTTP request example using Integrates.

This example demonstrates how to make basic HTTP requests using the Integrates Client.
"""

import asyncio

import integrates as api


def sync_example():
    """Example using the synchronous client."""
    # Create a client
    client = api.Client()

    # Make a GET request
    response = client.get("https://httpbin.org/get", params={"key": "value"})
    print(f"GET Status Code: {response.status_code}")
    print(f"Response JSON: {response.json()}")

    # Make a POST request with JSON data
    response = client.post(
        "https://httpbin.org/post", json={"name": "Integrates", "type": "API Client"}
    )
    print(f"POST Status Code: {response.status_code}")
    print(f"Response JSON: {response.json()}")

    # Using the context manager
    with api.Client() as client:
        response = client.get(
            "https://httpbin.org/headers", headers={"X-Custom-Header": "Integrates"}
        )
        print(f"Headers Status Code: {response.status_code}")
        print(f"Custom header echoed: {response.json()}")


async def async_example():
    """Example using the asynchronous client."""
    # Create an async client
    async with api.AsyncClient() as client:
        # Make a GET request
        response = await client.get("https://httpbin.org/get", params={"key": "value"})
        print(f"Async GET Status Code: {response.status_code}")
        print(f"Async Response JSON: {response.json()}")

        # Make a POST request with JSON data
        response = await client.post(
            "https://httpbin.org/post", json={"name": "Integrates Async", "type": "API Client"}
        )
        print(f"Async POST Status Code: {response.status_code}")
        print(f"Async Response JSON: {response.json()}")


if __name__ == "__main__":
    print("Running synchronous example:")
    sync_example()

    print("\nRunning asynchronous example:")
    asyncio.run(async_example())
