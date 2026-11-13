def find_permutation(n, k):
    # Start with a sorted permutation
    permutation = list(range(1, n + 1))
    
    # We need to create exactly k inversions
    # An inversion is a pair (i, j) such that i < j and permutation[i] > permutation[j]
    # We can achieve this by reversing the last k+1 elements of the sorted permutation
    
    # Reverse the last k+1 elements
    permutation[-k-1:] = reversed(permutation[-k-1:])
    
    # Print the result
    print(' '.join(map(str, permutation)))

# Read input
n, k = map(int, input().split())

# Find and print the permutation
find_permutation(n, k)