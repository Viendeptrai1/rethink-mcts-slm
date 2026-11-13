from itertools import combinations
import sys

def find_possible_values(n, k, coins):
    possible_values = set()
    
    # Generate all subsets of coins
    for r in range(1, n + 1):
        for combo in combinations(coins, r):
            if sum(combo) == k:
                # Check all subsets of this subset
                for i in range(1 << len(combo)):
                    subset_sum = sum(combo[j] for j in range(len(combo)) if (i & (1 << j)))
                    possible_values.add(subset_sum)
                    
    return sorted(possible_values)

# Input reading
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
coins = list(map(int, data[2:]))

# Find possible values
result = find_possible_values(n, k, coins)

# Output
print(len(result))
for value in result:
    print(value, end=' ')