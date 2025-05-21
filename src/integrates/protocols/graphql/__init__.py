"""
GraphQL protocol adapter for Integrates.
"""

from integrates.protocols.graphql.client import AsyncGraphQLClient, GraphQLClient

__all__ = [
    "GraphQLClient",
    "AsyncGraphQLClient",
]
