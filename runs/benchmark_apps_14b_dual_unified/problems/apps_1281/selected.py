import sys

def max_segments(n, k, a):
    # Calculate prefix XOR array
    prefix_xor = [0] * (n + 1)
    for i in range(1, n + 1):
        prefix_xor[i] = prefix_xor[i - 1] ^ a[i - 1]
    
    # Count initial segments with XOR != 0
    initial_count = 0
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            if prefix_xor[j] ^ prefix_xor[i - 1] != 0:
                initial_count += 1
    
    # Function to calculate XOR of a segment
    def xor_segment(l, r):
        return prefix_xor[r] ^ prefix_xor[l - 1]
    
    # Try flipping each element and count the new segments
    max_segments = initial_count
    for i in range(1, n + 1):
        flipped_value = a[i - 1] ^ ((1 << k) - 1)
        new_prefix_xor = prefix_xor[:]
        new_prefix_xor[i] = new_prefix_xor[i - 1] ^ flipped_value
        
        new_count = 0
        for j in range(1, n + 1):
            for l in range(1, j + 1):
                if xor_segment(l, j) != 0:
                    new_count += 1
        
        max_segments = max(max_segments, new_count)
    
    return max_segments

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:]))

# Output the result
print(max_segments(n, k, a))