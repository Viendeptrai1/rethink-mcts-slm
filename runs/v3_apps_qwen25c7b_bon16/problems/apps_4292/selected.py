def min_total_price(N, K, prices):
    # Sort the list of prices in ascending order
    sorted_prices = sorted(prices)
    
    # Calculate the sum of the first K elements after sorting
    min_price = sum(sorted_prices[:K])
    
    return min_price

# Read input from standard input
import sys
input = sys.stdin.read
data = input().split()

# Parse input
N = int(data[0])
K = int(data[1])
prices = list(map(int, data[2:]))

# Get the result
result = min_total_price(N, K, prices)

# Print the result
print(result)