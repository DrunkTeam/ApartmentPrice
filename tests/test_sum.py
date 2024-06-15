from src.dummy import sum

def test_sum_pn():
    x = 1
    y = -1

    result = sum(x, y)

    assert result == 0

def test_sum_pp():
    x = 1
    y = 1

    result = sum(x, y)

    assert result > 2