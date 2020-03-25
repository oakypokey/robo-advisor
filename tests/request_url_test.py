from app.robo_advisor import compile_url

def test_complile_url_MSFT():
    result = compile_url("MSFT").split("&")
    result.pop()
    result = "&".join(result)
    assert result == "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&datatype=json"

def test_complile_url_GOOG():
    result = compile_url("GOOG").split("&")
    result.pop()
    result = "&".join(result)
    assert result == "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=GOOG&datatype=json"

def test_complile_url_APPL():
    result = compile_url("APPL").split("&")
    result.pop()
    result = "&".join(result)
    assert result == "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=APPL&datatype=json"