import sys
from collections import defaultdict

def count_median_pairs(n, m, p):
    # Create a list to store the positions of each number in the permutation
    positions = defaultdict(list)
    for i in range(n):
        positions[p[i]].append(i)
    
    # Initialize variables to keep track of the counts of numbers less than, equal to, and greater than m
    less_count = [0] * (n + 1)
    equal_count = [0] * (n + 1)
    greater_count = [0] * (n + 1)
    
    # Fill the count arrays
    for i in range(1, n + 1):
        less_count[i] = less_count[i - 1]
        equal_count[i] = equal_count[i - 1]
        greater_count[i] = greater_count[i - 1]
        
        if p[i - 1] < m:
            less_count[i] += 1
        elif p[i - 1] == m:
            equal_count[i] += 1
        else:
            greater_count[i] += 1
    
    # Function to get the count of numbers less than, equal to, and greater than m in the range [l, r]
    def get_counts(l, r):
        return (less_count[r] - less_count[l - 1], equal_count[r] - equal_count[l - 1], greater_count[r] - greater_count[l - 1])
    
    # Initialize the result
    result = 0
    
    # Iterate over all possible right endpoints
    for r in range(1, n + 1):
        # Find the position of m in the current range
        m_pos = positions[m][0]
        
        # Calculate the required counts for the median to be m
        required_less = (r - m_pos) // 2
        required_equal = (r - m_pos) % 2
        
        # Iterate over all possible left endpoints
        for l in range(1, r + 1):
            less, equal, greater = get_counts(l, r)
            
            # Check if the current range has the required counts
            if less <= required_less and equal >= required_equal:
                result += 1
    
    return result

# Read input
n, m = map(int, sys.stdin.readline().split())
p = list(map(int, sys.stdin.readline().split()))

# Print the result
print(count_median_pairs(n, m, p))