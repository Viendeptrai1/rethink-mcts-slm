import sys
from collections import Counter

def count_triples(N, K):
    count = 0
    mod_counts = [Counter() for _ in range(K)]
    
    # Count occurrences of each remainder when divided by K
    for i in range(1, N + 1):
        mod_counts[i % K][i] += 1
    
    # Calculate the number of valid triples
    for a in mod_counts[0]:
        for b in mod_counts[(K - (a % K)) % K]:
            for c in mod_counts[a % K]:
                count += mod_counts[b % K][c]
                
    return count

# Read input from stdin
input = sys.stdin.read
data = input().split()

# Parse input
N = int(data[0])
K = int(data[1])

# Get result
result = count_triples(N, K)

# Print result
print(result)