def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    q = int(data[1])
    
    a = list(map(int, data[2:n+2]))
    b = list(map(int, data[n+2:n+2+q]))
    
    # Find all unique coin values
    unique_coins = sorted(set(a))
    
    # Precompute the minimum number of coins needed for each value up to the maximum query value
    max_b = max(b)
    min_coins = [-1] * (max_b + 1)
    min_coins[0] = 0  # Base case: 0 coins needed to make value 0
    
    for value in range(1, max_b + 1):
        for coin in unique_coins:
            if coin <= value and min_coins[value - coin] != -1:
                if min_coins[value] == -1:
                    min_coins[value] = min_coins[value - coin] + 1
                else:
                    min_coins[value] = min(min_coins[value], min_coins[value - coin] + 1)
    
    # Answer each query
    results = []
    for query in b:
        results.append(min_coins[query])
    
    # Print results
    for result in results:
        print(result)