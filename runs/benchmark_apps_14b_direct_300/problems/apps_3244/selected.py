def reconstruct_ring(N, sums):
    # Initialize the original ring with zeros
    original = [0] * N
    
    # Calculate the sum of all elements in the original ring
    total_sum = sum(sums) // 2
    
    # Calculate the first element of the original ring
    original[0] = (sums[0] + sums[-1] - sums[1]) // 2
    
    # Reconstruct the original ring
    for i in range(1, N):
        original[i] = sums[i-1] - original[i-1]
    
    return original

# Read input
import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
sums = list(map(int, data[1:]))

# Reconstruct the original ring
original_ring = reconstruct_ring(N, sums)

# Print the original ring
for num in original_ring:
    print(num)