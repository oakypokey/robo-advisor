from app.robo_advisor import get_response
from app.robo_advisor import compile_url

def test_get_response_metadata():
    result = get_response(compile_url("MSFT"))
    print(result)
    assert result.get('Meta Data', False)

def test_get_response_timeseries():
    result = get_response(compile_url("MSFT"))
    print(result)
    assert result.get("Time Series (Daily)", False)