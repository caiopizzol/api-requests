"""
REST protocol adapter for Integrates.
"""

from integrates.protocols.rest.client import AsyncRestClient, RestClient

__all__ = [
    "RestClient",
    "AsyncRestClient",
]
