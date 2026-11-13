def fib4(n: int) -> int:
    if n < 4:
        return [0, 0, 2, 0][n]
    
    dp = [0, 0, 2, 0]
    for _ in range(4, n + 1):
        dp.append(sum(dp[-4:]))
        dp.pop(0)
    
    return dp[-1]