import sys
from collections import defaultdict

def max_segments(n, k, a):
    # Initialize prefix XOR array
    prefix_xor = [0] * (n + 1)
    for i in range(1, n + 1):
        prefix_xor[i] = prefix_xor[i - 1] ^ a[i - 1]
    
    # Count occurrences of each prefix XOR value
    xor_count = defaultdict(int)
    xor_count[0] = 1
    
    # Calculate the initial number of valid segments
    valid_segments = 0
    for i in range(1, n + 1):
        valid_segments += i - xor_count[prefix_xor[i]]
        xor_count[prefix_xor[i]] += 1
    
    # Try flipping each bit position
    for bit in range(k):
        new_xor_count = defaultdict(int)
        new_xor_count[0] = 1
        new_valid_segments = 0
        flip = 1 << bit
        
        for i in range(1, n + 1):
            new_prefix_xor = prefix_xor[i] ^ flip
            new_valid_segments += i - new_xor_count[new_prefix_xor]
            new_xor_count[new_prefix_xor] += 1
        
        valid_segments = max(valid_segments, new_valid_segments)
    
    return valid_segments

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:]))

# Output the result
print(max_segments(n, k, a))