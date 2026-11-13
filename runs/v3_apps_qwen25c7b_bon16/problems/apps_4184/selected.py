import sys
from itertools import combinations

def min_weight_difference(N, weights):
    min_diff = float('inf')
    for t in range(1, N):
        S1 = sum(weights[:t])
        S2 = sum(weights[t:])
        diff = abs(S1 - S2)
        if diff < min_diff:
            min_diff = diff
    return min_diff

# Read input
input = sys.stdin.read
data = input().split()
N = int(data[0])
weights = list(map(int, data[1:]))

# Calculate and print the result
print(min_weight_difference(N, weights))