from app.robo_advisor import get_response
from app.robo_advisor import compile_url
import os
import pytest

CI_ENV = os.environ.get("CI") == "true"

@pytest.mark.skipif(CI_ENV==True, reason="to avoid issuing HTTP requests on the CI server") # skips this test on CI
def test_get_response_metadata(stock_data):
    result = stock_data
    assert result.get('Meta Data', False)

@pytest.mark.skipif(CI_ENV==True, reason="to avoid issuing HTTP requests on the CI server") # skips this test on CI
def test_get_response_timeseries(stock_data):
    result = stock_data
    assert result.get("Time Series (Daily)", False)