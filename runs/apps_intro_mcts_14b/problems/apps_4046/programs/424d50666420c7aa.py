import sys

def restore_permutation(n, q):
    # Check if the sum of all elements in q is zero
    if sum(q) != 0:
        return [-1]
    
    # Initialize the permutation with the first element as 0
    p = [0]
    
    # Construct the permutation based on the differences
    for i in range(1, n):
        p.append(p[-1] + q[i-1])
    
    # Check if the permutation contains all numbers from 1 to n exactly once
    used = [False] * (n + 1)
    for value in p:
        if value < 1 or value > n or used[value]:
            return [-1]
        used[value] = True
    
    return p

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
q = list(map(int, data[1:]))

# Restore the permutation
result = restore_permutation(n, q)

# Print the result
print(" ".join(map(str, result)))