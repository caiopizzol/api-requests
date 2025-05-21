"""
GraphQL protocol adapter for API Requests.
"""

from api_requests.protocols.graphql.client import AsyncGraphQLClient, GraphQLClient

__all__ = [
    "GraphQLClient",
    "AsyncGraphQLClient",
]
