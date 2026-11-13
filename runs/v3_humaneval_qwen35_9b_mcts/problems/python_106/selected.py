def f(n):
    result = []
    for i in range(1, n + 1):
        if i % 2 == 0:
            # i is even: compute factorial of i
            fact = 1
            for j in range(1, i + 1):
                fact *= j
            result.append(fact)
        else:
            # i is odd: compute sum from 1 to i
            total = i * (i + 1) // 2
            result.append(total)
    return result