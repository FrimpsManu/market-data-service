from app.utils.moving_average import calculate_moving_average 

def test_calculate_moving_average_basic():
    prices = [100, 101, 99, 102, 98]
    assert calculate_moving_average(prices) == 100

def test_calculate_moving_average_empty():
    prices = []
    assert calculate_moving_average(prices) is None

def test_calculate_moving_average_single_value():
    prices = [120]
    assert calculate_moving_average(prices) == 120

def test_calculate_moving_average_precision():
    prices = [100, 101, 102]
    result = calculate_moving_average(prices)
    assert round(result, 2) == 101.0
