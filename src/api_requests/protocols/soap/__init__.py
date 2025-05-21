"""
SOAP protocol adapter for API Requests.
"""

from api_requests.protocols.soap.client import AsyncSoapClient, SoapClient

__all__ = [
    "SoapClient",
    "AsyncSoapClient",
]
