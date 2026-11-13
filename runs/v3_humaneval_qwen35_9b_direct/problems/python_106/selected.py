def f(n):
    result = []
    factorial = 1
    for i in range(1, n + 1):
        if i % 2 == 0:
            factorial *= i
            result.append(factorial)
        else:
            result.append(i * (i + 1) // 2)
    return result