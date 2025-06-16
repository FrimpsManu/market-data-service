def calculate_moving_average(prices):
    if not prices:
        return None
    return sum(prices) / len(prices)
