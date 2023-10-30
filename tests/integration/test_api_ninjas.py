from quotes.request_quote import extract_quote


def test_integration_with_api_ninjas(api_key_integration):
    """
    Test the integration with the Ninjas API using a real API key.

    This test verifies that the function 'extract_quote' successfully connects to the
    Ninjas API using the provided real API key and returns a real quote from the API.

    Args:
        api_key_integration (str): A real API key obtained from environment variables.
        # The 'api_key_integration' argument is a fixture defined in `conftest.py` for this test.

    Test Steps:
    1. Given the REAL API key coming from environment variables.
    2. When I call the function 'extract_quote' with the real API key.
    3. The function should return a list containing at least one dictionary.
    4. The 'quote' field in the returned dictionary must be a string.

    This test ensures that the 'extract_quote' function works correctly when interacting with
    the Ninjas API and handles the API key properly.
    """
    real_api_key = api_key_integration
    real_quote = extract_quote(API_KEY=real_api_key)
    quote = real_quote[0].get("quote")

    # Assertions
    assert isinstance(real_quote, list)
    assert isinstance(quote, str)
