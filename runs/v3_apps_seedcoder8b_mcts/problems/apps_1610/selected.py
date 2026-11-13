def find_permutation(n, k):
    # Create the first k decreasing pairs
    permutation = list(range(1, n - k + 1))
    
    # Fill the rest of the permutation in ascending order
    remaining = list(range(n - k + 1, n + 1))
    permutation.extend(remaining)
    
    # Reverse the last k+1 elements to ensure exactly k decreasing pairs
    permutation[-k-1:] = reversed(permutation[-k-1:])
    
    return permutation

# Read input
n, k = map(int, input().split())

# Find and print the permutation
result = find_permutation(n, k)
print(*result)