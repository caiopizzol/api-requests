import json
import pytest
from unittest.mock import MagicMock
from integrates.core.response import Response


@pytest.fixture
def mock_response():
    """Create a factory function for Response objects."""

    def _create_response(
        status_code=200,
        headers=None,
        content=None,
        url="https://example.com",
        json_data=None,
        request_info=None,
        encoding="utf-8",
    ):
        if json_data is not None:
            content = json.dumps(json_data).encode("utf-8")
        elif content is None:
            content = b""

        return Response(
            status_code=status_code,
            headers=headers or {},
            content=content,
            url=url,
            request_info=request_info,
            encoding=encoding,
        )

    return _create_response


@pytest.fixture
def mock_httpx_client():
    client = MagicMock()
    return client
