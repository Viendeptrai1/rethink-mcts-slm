def find_permutation_q(n, p):
    # Create an array to store the inverse of p
    q = [0] * n
    
    # Fill the inverse array
    for i in range(n):
        q[p[i] - 1] = i + 1
    
    # Check if q^2 equals p
    for i in range(n):
        if q[q[i] - 1] != p[i]:
            return [-1]
    
    return q

# Read input
n = int(input())
p = list(map(int, input().split()))

# Find permutation q
result = find_permutation_q(n, p)

# Print the result
if result == [-1]:
    print(-1)
else:
    print(*result)