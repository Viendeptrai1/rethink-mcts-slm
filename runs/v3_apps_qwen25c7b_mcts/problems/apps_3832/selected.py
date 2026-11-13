import sys
from math import ceil

def min_hours_to_build_houses(n, hills):
    max_k = ceil(n / 2)
    results = [0] * max_k
    
    for k in range(1, max_k + 1):
        min_operations = float('inf')
        
        for start in range(n - k + 1):
            current_operations = 0
            for i in range(start, start + k):
                if i > 0 and hills[i] <= hills[i - 1]:
                    current_operations += hills[i - 1] - hills[i] + 1
                if i < n - 1 and hills[i] <= hills[i + 1]:
                    current_operations += hills[i + 1] - hills[i] + 1
            min_operations = min(min_operations, current_operations)
        
        results[k - 1] = min_operations
    
    return results

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
hills = list(map(int, data[1:]))

# Get results
results = min_hours_to_build_houses(n, hills)

# Print results
print(" ".join(map(str, results)))