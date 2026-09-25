import sys
from collections import deque

def count_median_pairs(n, m, p):
    # Find all positions of m in the permutation
    positions = [i for i in range(n) if p[i] == m]
    
    # If there are no positions of m, return 0
    if not positions:
        return 0
    
    # Initialize the result
    result = 0
    
    # For each position of m, calculate the number of valid subarrays
    for mid in positions:
        # Count elements less than m to the left of mid
        less_count = 0
        for i in range(mid - 1, -1, -1):
            if p[i] < m:
                less_count += 1
        
        # Count elements greater than m to the right of mid
        greater_count = 0
        for i in range(mid + 1, n):
            if p[i] > m:
                greater_count += 1
        
        # Calculate the number of valid subarrays ending at mid
        valid_subarrays = (less_count + 1) * (greater_count + 1)
        
        # Add to the result
        result += valid_subarrays
    
    return result

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
m = int(data[1])
p = list(map(int, data[2:]))

# Output the result
print(count_median_pairs(n, m, p))