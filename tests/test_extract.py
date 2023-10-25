import pytest

from quotes.request_quote import extract_quote, pick_random_category, save_to_storage


def test_return_one_string_randomly_between_list_of_categories():
    # Give a list of countries

    country_list = ["Germany", "Brazil", "Portugal", "India"]

    # When I call my function to pick one randoly
    random_country = pick_random_category(country_list)
    # Then should pick one and this value should be at the list
    assert random_country in country_list
    assert isinstance(random_country, str)


def test_if_quote_return_string_when_success(mocker):
    # Given the status code of sucess
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    # mock_response.text["This is a quote"]
    mock_response.json.return_value = ["This is a quote"]
    mocker.patch("requests.get", return_value=mock_response)

    # Mock the authenticate_databricks function because I am not interested to test it
    mocker.patch("quotes.request_quote.authenticate_databricks")

    # When we can the function and run succes
    quote = extract_quote()

    # Then the type should be json
    assert isinstance(quote, list)


def test_log_error_when_function_return_400(mocker, caplog):
    # Given the response returning 400, because we are mocking it
    mock_response = mocker.Mock()
    mock_response.status_code = 400
    mock_response.text = "Bad Request"
    mocker.patch("requests.get", return_value=mock_response)

    # Mock the authenticate_databricks function because I am not interested to test it
    mocker.patch("quotes.request_quote.authenticate_databricks")

    # When we call the function will generate wrong status_code
    extract_quote()

    # Then the log Message should be checked
    expected_log_message = (
        f"Status Code: {mock_response.status_code} - Reason: {mock_response.text}"
    )
    assert expected_log_message in caplog.text


def test_if_data_is_none_will_not_save_to_storage_and_let_user_know(caplog):
    # Given the Data which is null and a path to save
    data = None
    path = "/mnt/fake/path"

    # When we call the function to save to storage, the data will be None
    save_to_storage(data=data, path_dbfs=path)

    # Then the code must return a logging
    # informing the data is None

    expected_log_message = "Data returned None"
    result_log = caplog.text
    assert expected_log_message in result_log


if __name__ == "__main__":
    pytest.main()
