"""
Exception classes for API Requests.
"""

from typing import Optional

from api_requests.core.response import Response


class APIRequestsError(Exception):
    """Base exception for all API Requests errors."""

    pass


class TransportError(APIRequestsError):
    """Error during HTTP transport."""

    pass


class TimeoutError(TransportError):
    """Request timed out."""

    pass


class HTTPError(APIRequestsError):
    """HTTP error response."""

    def __init__(self, message: str, response: Optional[Response] = None):
        """
        Initialize an HTTPError.

        Args:
            message: Error message
            response: Response that caused the error
        """
        super().__init__(message)
        self.response = response

    @property
    def status_code(self) -> Optional[int]:
        """Return the status code of the response, if available."""
        return self.response.status_code if self.response else None


class SchemaValidationError(APIRequestsError):
    """Error validating response against schema."""

    pass
