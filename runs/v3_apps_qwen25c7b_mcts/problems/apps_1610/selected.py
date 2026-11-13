def generate_permutation(n, k):
    # Create the base permutation [1, 2, ..., n]
    perm = list(range(1, n + 1))
    
    # Place the largest k+1 numbers in reverse order at the beginning
    perm[:k+1] = reversed(perm[:k+1])
    
    return perm

# Read input
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])

# Generate and print the permutation
result = generate_permutation(n, k)
print(' '.join(map(str, result)))