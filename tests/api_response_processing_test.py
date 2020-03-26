from app.robo_advisor import StockData
from app.robo_advisor import get_response
from app.robo_advisor import compile_url
import os
import pytest

test_response = {
    "Meta Data": {
        "1. Information": "Daily Prices (open, high, low, close) and Volumes",
        "2. Symbol": "TEST",
        "3. Last Refreshed": "2018-06-08",
        "4. Output Size": "Full size",
        "5. Time Zone": "US/Eastern"
    },
    "Time Series (Daily)": {
        "2019-06-08": {
            "1. open": "101.0924",
            "2. high": "101.9500",
            "3. low": "100.5400",
            "4. close": "101.6300",
            "5. volume": "22165128"
        },
        "2019-06-07": {
            "1. open": "102.6500",
            "2. high": "102.6900",
            "3. low": "100.3800",
            "4. close": "100.8800",
            "5. volume": "28232197"
        },
        "2019-06-06": {
            "1. open": "102.4800",
            "2. high": "102.6000",
            "3. low": "101.9000",
            "4. close": "102.4900",
            "5. volume": "21122917"
        }
    }
}

def test_process_data():  
    try:
        data = StockData(test_response)
        result = data.get_stats()

        assert type(result["latest_close"]) == float
        assert isinstance(result, dict)
        assert result["average_price"] == 101.66666666666667
        assert result["recent_high"] == 102.69
        assert result["recent_low"] == 101.9
    
    except:
        assert False