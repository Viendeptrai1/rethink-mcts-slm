def special_factorial(n):
    from functools import lru_cache

    @lru_cache(None)
    def factorial(x):
        if x == 0 or x == 1:
            return 1
        return x * factorial(x - 1)

    if n <= 0:
        return 0

    result = 1
    for i in range(1, n + 1):
        result *= factorial(i)

    return result