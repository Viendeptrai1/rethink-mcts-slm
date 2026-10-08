from itertools import combinations

def solve(n, k, coins):
    # Find all subsets that sum to k
    valid_subsets = []
    for r in range(1, n + 1):
        for subset in combinations(coins, r):
            if sum(subset) == k:
                valid_subsets.append(subset)
    
    # Find all possible sums that can be formed from these subsets
    possible_sums = set()
    for subset in valid_subsets:
        for r in range(len(subset) + 1):
            for subsubset in combinations(subset, r):
                possible_sums.add(sum(subsubset))
    
    # Convert the set to a sorted list
    possible_sums = sorted(list(possible_sums))
    
    # Print the result
    print(len(possible_sums))
    print(" ".join(map(str, possible_sums)))

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
coins = list(map(int, data[2:]))

# Solve the problem
solve(n, k, coins)