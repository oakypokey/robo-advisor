import pytest
from app.robo_advisor import get_response, compile_url

@pytest.fixture(scope="session")
def stock_data():
    return get_response(compile_url("MSFT"))