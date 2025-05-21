"""
SOAP protocol adapter for Integrates.
"""

from integrates.protocols.soap.client import AsyncSoapClient, SoapClient

__all__ = [
    "SoapClient",
    "AsyncSoapClient",
]
