import sys

def max_segments(n, k, a):
    # Calculate prefix XORs
    prefix_xor = [0] * (n + 1)
    for i in range(1, n + 1):
        prefix_xor[i] = prefix_xor[i - 1] ^ a[i - 1]
    
    # Count occurrences of each prefix XOR
    xor_count = {}
    for xor_val in prefix_xor:
        if xor_val in xor_count:
            xor_count[xor_val] += 1
        else:
            xor_count[xor_val] = 1
    
    # Calculate the maximum number of segments
    max_segments = 0
    for xor_val, count in xor_count.items():
        max_segments += count * (count - 1) // 2
    
    return max_segments

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:]))

# Output the result
print(max_segments(n, k, a))