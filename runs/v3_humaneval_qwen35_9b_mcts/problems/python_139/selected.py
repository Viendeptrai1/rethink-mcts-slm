def special_factorial(n):
    result = 1
    current_factorial = 1
    for i in range(1, n + 1):
        current_factorial *= i
        result *= current_factorial
    return result