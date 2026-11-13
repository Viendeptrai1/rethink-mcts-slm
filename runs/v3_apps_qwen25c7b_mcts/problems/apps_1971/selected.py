def find_inverse_permutation(n, p):
    # Create a list to store the result permutation q
    q = [-1] * n
    
    # Create a dictionary to map each value in p to its index
    index_map = {p[i]: i for i in range(n)}
    
    # Iterate through each element in p
    for i in range(n):
        next_index = p[i]
        target_value = p[next_index - 1]
        
        # Check if the current position is already assigned or if it would cause a conflict
        while q[target_value - 1] != -1:
            target_value = q[target_value - 1]
        
        # Assign the value to the correct position
        q[target_value - 1] = i + 1
    
    # Verify if the constructed permutation satisfies the condition q^2 = p
    for i in range(n):
        if q[q[i] - 1] != p[i]:
            return -1
    
    return q

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
p = list(map(int, data[1:]))

# Find the inverse permutation
result = find_inverse_permutation(n, p)

# Print the result
if result == -1:
    print(-1)
else:
    print(' '.join(map(str, result)))