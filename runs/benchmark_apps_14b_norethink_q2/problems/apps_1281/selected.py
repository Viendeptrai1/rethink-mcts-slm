import sys
from collections import defaultdict

def max_segments(n, k, a):
    # Calculate the prefix XORs
    prefix_xor = [0] * (n + 1)
    for i in range(1, n + 1):
        prefix_xor[i] = prefix_xor[i - 1] ^ a[i - 1]
    
    # Count the number of valid segments without any operations
    count = 0
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            if prefix_xor[j] ^ prefix_xor[i - 1] != 0:
                count += 1
    
    # Function to flip a k-bit integer
    def flip(x):
        return (1 << k) - 1 - x
    
    # Try flipping each element and see how it affects the count
    for i in range(n):
        new_a = a[:]
        new_a[i] = flip(new_a[i])
        
        new_prefix_xor = [0] * (n + 1)
        for j in range(1, n + 1):
            new_prefix_xor[j] = new_prefix_xor[j - 1] ^ new_a[j - 1]
        
        new_count = 0
        for i in range(1, n + 1):
            for j in range(i, n + 1):
                if new_prefix_xor[j] ^ new_prefix_xor[i - 1] != 0:
                    new_count += 1
        
        count = max(count, new_count)
    
    return count

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:]))

# Output the result
print(max_segments(n, k, a))