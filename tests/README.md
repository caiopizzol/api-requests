# Integrates Test Suite

This directory contains tests for the Integrates library. The tests are organized by module and use pytest as the test runner.

## Running the Tests

### Using Tox (Recommended)

To run tests across multiple Python versions:

```bash
# Run tests on all supported Python versions
tox

# Run tests on a specific Python version
tox -e py310

# Run tests with specific arguments
tox -- -xvs tests/test_client.py
```

### Using pytest directly

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_client.py

# Run with verbose output
pytest -v

# Run with code coverage
pytest --cov=integrates
```

## Test Organization

- `conftest.py`: Common fixtures used across multiple test files
- `test_client.py`: Tests for the core Client class
- `test_async_client.py`: Tests for the AsyncClient class
- `test_response.py`: Tests for the Response class
- `test_auth.py`: Tests for the authentication modules
- `test_middleware.py`: Tests for middleware functionality
- `test_rest_client.py`: Tests for the REST client implementation
- `test_graphql_client.py`: Tests for the GraphQL client implementation

## Writing New Tests

When adding new functionality to the library, please add corresponding tests. Follow these guidelines:

1. Place tests in the appropriate file based on the module being tested
2. Use appropriate fixtures from `conftest.py`
3. Mock external dependencies
4. Test both success and error cases
5. Follow the naming convention: `test_<functionality>_<scenario>`
