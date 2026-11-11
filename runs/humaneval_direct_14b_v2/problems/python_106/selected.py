def f(n):
    def factorial(x):
        return 1 if x == 0 or x == 1 else x * factorial(x - 1)
    
    def sum_to(x):
        return x * (x + 1) // 2
    
    result = []
    for i in range(1, n + 1):
        if i % 2 == 0:
            result.append(factorial(i))
        else:
            result.append(sum_to(i))
    
    return result