from quotes_dbx.request_quote import extract_quote


def test_if_quote_return_string_when_success():
    ...
    # Given the status code of sucess

    # When we can the function and run succes
    quote = extract_quote()

    # Then the type should be json
    assert isinstance(quote, str)
