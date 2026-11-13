def reconstruct_original_ring(N, sums):
    # Initialize the original ring with zeros
    original = [0] * N
    
    # Calculate the first element of the original ring
    original[0] = sums[0] - sums[N-1]
    
    # Calculate the rest of the elements
    for i in range(1, N):
        original[i] = sums[i] - original[i-1]
    
    return original

# Read input
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
sums = list(map(int, data[1:]))

# Reconstruct the original ring
original_ring = reconstruct_original_ring(N, sums)

# Print the result
for num in original_ring:
    print(num)