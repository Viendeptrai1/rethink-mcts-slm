import sys
from collections import defaultdict

def max_segments(n, k, a):
    # Calculate prefix XORs
    prefix_xor = [0] * (n + 1)
    for i in range(1, n + 1):
        prefix_xor[i] = prefix_xor[i - 1] ^ a[i - 1]
    
    # Count occurrences of each prefix XOR
    xor_count = defaultdict(int)
    xor_count[0] = 1
    
    # Calculate the maximum number of segments
    max_segments = 0
    for i in range(1, n + 1):
        max_segments += i - xor_count[prefix_xor[i]]
        xor_count[prefix_xor[i]] += 1
    
    # Calculate the number of segments that would be lost if we flip each element
    flip_count = defaultdict(int)
    flip_count[0] = 1
    for i in range(1, n + 1):
        flipped_xor = prefix_xor[i] ^ ((1 << k) - 1)
        max_segments -= flip_count[flipped_xor]
        flip_count[flipped_xor] += 1
    
    return max_segments

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:]))

# Output the result
print(max_segments(n, k, a))