def fibfib(n: int) -> int:
    memo = {0: 0, 1: 0, 2: 1}
    
    def helper(x):
        if x not in memo:
            memo[x] = helper(x - 1) + helper(x - 2) + helper(x - 3)
        return memo[x]
    
    return helper(n)