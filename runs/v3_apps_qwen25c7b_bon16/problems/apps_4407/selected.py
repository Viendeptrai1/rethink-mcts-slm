def min_coins_to_value(coins, target):
    dp = [float('inf')] * (target + 1)
    dp[0] = 0
    
    for coin in coins:
        for j in range(target, coin - 1, -1):
            dp[j] = min(dp[j], dp[j - coin] + 1)
    
    return dp[target]

def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    q = int(data[1])
    
    coins = list(map(int, data[2:2+n]))
    targets = list(map(int, data[2+n:]))
    
    results = []
    for target in targets:
        result = min_coins_to_value(coins, target)
        if result == float('inf'):
            results.append(-1)
        else:
            results.append(result)
    
    print(*results)

if __name__ == "__main__":
    solve()