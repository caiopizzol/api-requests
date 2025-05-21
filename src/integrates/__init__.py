"""
Integrates - A requests-style, protocol-agnostic SDK for API integration

This package provides a simple, ergonomic interface for interacting with
various API protocols (REST, GraphQL, SOAP) while maintaining the familiar
feel of the Python 'requests' library.
"""

__version__ = "0.1.0"

import integrates.auth as auth
import integrates.middleware as middleware
from integrates.core.client import AsyncClient, Client
from integrates.core.response import Response
from integrates.protocols.graphql import AsyncGraphQLClient, GraphQLClient
from integrates.protocols.rest import AsyncRestClient, RestClient
from integrates.protocols.soap import AsyncSoapClient, SoapClient

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
