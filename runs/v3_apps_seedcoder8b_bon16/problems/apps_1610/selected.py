def find_permutation(n, k):
    # Create a base permutation from 1 to n
    permutation = list(range(1, n + 1))
    
    # Reverse the first k+1 elements to create the desired decreasing coefficient
    permutation[:k+1] = reversed(permutation[:k+1])
    
    # Print the resulting permutation
    print(' '.join(map(str, permutation)))

# Read input
import sys
input_data = sys.stdin.read().strip()
n, k = map(int, input_data.split())

# Find and print the permutation
find_permutation(n, k)