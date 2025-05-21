"""
Authentication methods for Integrates.
"""

from integrates.auth.api_key import ApiKeyAuth
from integrates.auth.base import Auth
from integrates.auth.basic import BasicAuth
from integrates.auth.bearer import BearerAuth
from integrates.auth.oauth2 import OAuth2

__all__ = [
    "Auth",
    "BasicAuth",
    "BearerAuth",
    "OAuth2",
    "ApiKeyAuth",
]
