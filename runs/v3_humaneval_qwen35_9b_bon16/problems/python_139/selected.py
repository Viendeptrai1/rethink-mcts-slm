def special_factorial(n):
    def factorial(x):
        if x <= 1:
            return 1
        result = 1
        for i in range(2, x + 1):
            result *= i
        return result

    result = 1
    for i in range(n, 0, -1):
        result *= factorial(i)
    return result