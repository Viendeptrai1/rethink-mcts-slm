def find_inverse_permutation(p):
    n = len(p)
    if n == 1:
        return p
    
    # Create a list to store the result
    q = [-1] * n
    
    # Iterate over the indices of the permutation
    for i in range(n):
        # Check if the current index is already filled or if the value at the current index is already used
        if q[i] != -1 or p[p[i]-1] != -1:
            continue
        
        # Find the cycle in the permutation
        cycle = []
        x = i
        while True:
            cycle.append(x)
            x = p[x]-1
            if x == i:
                break
        
        # Reverse the cycle to get the inverse permutation
        for j in range(len(cycle)):
            q[cycle[j]] = cycle[(j + len(cycle) // 2) % len(cycle)] + 1
    
    return q

# Read input from stdin
import sys
input = sys.stdin.read
data = input().split()

# Get the number of elements
n = int(data[0])

# Get the permutation
p = list(map(int, data[1:]))

# Find the inverse permutation
result = find_inverse_permutation(p)

# Print the result
if result[0] == -1:
    print(-1)
else:
    print(" ".join(map(str, result)))