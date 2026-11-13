def min_coins_to_value(coins, queries):
    # Create a list to store the minimum number of coins needed for each value up to max(queries)
    dp = [-1] * (max(queries) + 1)
    
    # Initialize the dp array with the base case where 0 value needs 0 coins
    dp[0] = 0
    
    # Fill the dp array with the minimum number of coins needed for each value
    for coin in coins:
        for i in range(len(dp)):
            if dp[i] != -1 and i + coin <= len(dp) - 1:
                if dp[i + coin] == -1 or dp[i + coin] > dp[i] + 1:
                    dp[i + coin] = dp[i] + 1
    
    # Return the results for each query
    return [dp[query] for query in queries]

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
q = int(data[1])

coins = list(map(int, data[2:2+n]))
queries = list(map(int, data[2+n:]))

# Get the results
results = min_coins_to_value(coins, queries)

# Print the results
for result in results:
    print(result)