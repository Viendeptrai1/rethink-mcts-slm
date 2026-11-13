def f(n):
    def factorial(x):
        if x == 0:
            return 1
        result = 1
        for i in range(1, x + 1):
            result *= i
        return result

    result_list = []
    for i in range(1, n + 1):
        if i % 2 == 0:
            result_list.append(factorial(i))
        else:
            result_list.append(sum(range(1, i + 1)))
    return result_list