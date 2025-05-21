"""
Authentication methods for API Requests.
"""

from api_requests.auth.api_key import ApiKeyAuth
from api_requests.auth.base import Auth
from api_requests.auth.basic import BasicAuth
from api_requests.auth.bearer import BearerAuth
from api_requests.auth.oauth2 import OAuth2

__all__ = [
    "Auth",
    "BasicAuth",
    "BearerAuth",
    "OAuth2",
    "ApiKeyAuth",
]
