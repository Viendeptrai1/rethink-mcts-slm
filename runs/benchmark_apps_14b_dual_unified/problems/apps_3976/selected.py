from collections import Counter

def find_valid_positions(n, m, p, a, b):
    # Count the frequency of each element in b
    b_count = Counter(b)
    
    valid_positions = []
    
    # Iterate over all possible starting positions q
    for q in range(1, n - (m - 1) * p + 1):
        # Extract the subsequence from a
        subsequence = [a[q - 1 + i * p] for i in range(m)]
        
        # Count the frequency of each element in the subsequence
        subsequence_count = Counter(subsequence)
        
        # Check if the subsequence can be rearranged to match b
        if subsequence_count == b_count:
            valid_positions.append(q)
    
    return len(valid_positions), valid_positions

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
p = int(data[2])
a = list(map(int, data[3:3+n]))
b = list(map(int, data[3+n:]))

# Find valid positions
num_valid_positions, valid_positions = find_valid_positions(n, m, p, a, b)

# Print the result
print(num_valid_positions)
print(*valid_positions)