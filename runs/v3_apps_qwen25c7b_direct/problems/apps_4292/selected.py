import sys

def min_total_price(N, K, prices):
    prices.sort()
    return sum(prices[:K])

# Read input
input = sys.stdin.read
data = input().split()

N = int(data[0])
K = int(data[1])
prices = list(map(int, data[2:]))

# Calculate and print the result
print(min_total_price(N, K, prices))