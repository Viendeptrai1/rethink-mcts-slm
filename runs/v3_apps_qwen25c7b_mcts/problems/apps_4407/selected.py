def min_coins(n, q, coins, queries):
    max_value = max(queries)
    dp = [-1] * (max_value + 1)
    dp[0] = 0
    
    for coin in coins:
        for j in range(max_value, coin - 1, -1):
            if dp[j - coin] != -1:
                dp[j] = dp[j] if dp[j] != -1 else dp[j - coin] + 1
    
    return [dp[b] for b in queries]

# Input reading
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
q = int(data[1])
coins = list(map(int, data[2:2+n]))
queries = list(map(int, data[2+n:]))

# Output the result
result = min_coins(n, q, coins, queries)
print(*result)