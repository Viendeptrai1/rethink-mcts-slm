import sys

def reconstruct_original_ring(N, ring):
    original_ring = []
    for i in range(N):
        original_value = ring[(i + 2) % N] - ring[i] - ring[(i + 1) % N]
        original_ring.append(original_value)
    return original_ring

# Read input
input = sys.stdin.read
data = input().split()

N = int(data[0])
ring = list(map(int, data[1:]))

# Reconstruct the original ring
original_ring = reconstruct_original_ring(N, ring)

# Print the result
for num in original_ring:
    print(num)