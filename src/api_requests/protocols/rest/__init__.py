"""
REST protocol adapter for API Requests.
"""

from api_requests.protocols.rest.client import AsyncRestClient, RestClient

__all__ = [
    "RestClient",
    "AsyncRestClient",
]
