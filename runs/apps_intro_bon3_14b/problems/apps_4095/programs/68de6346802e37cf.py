import sys
from collections import defaultdict

def count_median_pairs(n, m, p):
    # Create a list to store the positions of each element in the permutation
    positions = defaultdict(list)
    for i in range(n):
        positions[p[i]].append(i)
    
    # If m is not in the permutation, there are no valid pairs
    if m not in positions:
        return 0
    
    # Get the positions of m in the permutation
    m_positions = positions[m]
    
    # Initialize the count of valid pairs
    count = 0
    
    # Iterate over each position of m
    for i in range(len(m_positions)):
        # Count the number of elements less than m to the left of m_positions[i]
        less_count = sum(1 for pos in positions[k] if pos < m_positions[i] for k in range(1, m))
        
        # Count the number of elements greater than m to the right of m_positions[i]
        greater_count = sum(1 for pos in positions[k] if pos > m_positions[i] for k in range(m + 1, n + 1))
        
        # Calculate the number of valid subarrays ending at m_positions[i]
        valid_subarrays = (less_count + 1) * (greater_count + 1)
        
        # Add to the total count
        count += valid_subarrays
    
    return count

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
m = int(data[1])
p = list(map(int, data[2:]))

# Calculate and print the result
result = count_median_pairs(n, m, p)
print(result)