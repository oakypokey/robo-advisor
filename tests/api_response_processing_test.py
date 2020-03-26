from app.robo_advisor import StockData
from app.robo_advisor import get_response
from app.robo_advisor import compile_url
import os
import pytest

CI_ENV = os.environ.get("CI") == "true"

@pytest.mark.skipif(CI_ENV==True, reason="to avoid issuing HTTP requests on the CI server") # skips this test on CI
def test_process_data(stock_data):  
    try:
        data = StockData(stock_data)
        result = data.get_stats()

        assert type(result["latest_close"]) == float
        assert isinstance(result, dict)
    
    except:
        assert False