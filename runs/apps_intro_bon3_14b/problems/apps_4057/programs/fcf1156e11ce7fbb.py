import sys
from collections import Counter

def min_pockets(n, coins):
    # Count the frequency of each coin value
    coin_count = Counter(coins)
    
    # The minimum number of pockets needed is the maximum frequency of any coin value
    return max(coin_count.values())

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
coins = list(map(int, data[1:]))

# Calculate and print the result
print(min_pockets(n, coins))