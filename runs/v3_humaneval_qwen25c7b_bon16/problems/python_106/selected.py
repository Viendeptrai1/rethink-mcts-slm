def f(n):
    def factorial(x):
        return x * factorial(x - 1) if x > 1 else 1

    def sum_to_n(x):
        return x * (x + 1) // 2

    return [factorial(i) if i % 2 == 0 else sum_to_n(i) for i in range(1, n + 1)]