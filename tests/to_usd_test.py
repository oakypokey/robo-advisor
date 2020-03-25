from app.robo_advisor import to_usd

def test_to_usd_isZero():
    result = to_usd(0)
    assert result == '$0.00'

def test_to_usd_isSingleDigit():
    result = to_usd(1)
    assert result == '$1.00'

def test_to_usd_isDoubleDigit():
    result = to_usd(20)
    assert result == '$20.00'

def test_to_usd_isFloat():
    result = to_usd(1.23)
    assert result == '$1.23'

def test_to_usd_isLongFloat():
    result = to_usd(1.2345)
    assert result == '$1.23'

def test_to_usd_isNegative():
    result = to_usd(-1.23)
    assert result == '$-1.23'

def test_to_usd_thousandsSeperator():
    result = to_usd(1000)
    assert len(result.split(",")) > 1