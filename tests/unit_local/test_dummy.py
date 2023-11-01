from quotes.dummy import dummy_func


def test_dummy_func():
    # Given the expected return from my dummy func
    expected_message = "Dummy"

    # When I call function to return the Dummy text
    result = dummy_func()

    # Then the result should be the same
    assert expected_message == result
