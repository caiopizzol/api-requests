"""
API Requests - A requests-style, protocol-agnostic SDK for API integration

This package provides a simple, ergonomic interface for interacting with
various API protocols (REST, GraphQL, SOAP) while maintaining the familiar
feel of the Python 'requests' library.
"""

__version__ = "0.1.0"

import api_requests.auth as auth
import api_requests.middleware as middleware
from api_requests.core.client import AsyncClient, Client
from api_requests.core.response import Response
from api_requests.protocols.graphql import AsyncGraphQLClient, GraphQLClient
from api_requests.protocols.rest import AsyncRestClient, RestClient
from api_requests.protocols.soap import AsyncSoapClient, SoapClient

__all__ = [
    "Client",
    "AsyncClient",
    "Response",
    "auth",
    "middleware",
    "RestClient",
    "AsyncRestClient",
    "GraphQLClient",
    "AsyncGraphQLClient",
    "SoapClient",
    "AsyncSoapClient",
]
