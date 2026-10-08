import sys

def find_permutation(n, p):
    # Create a list of positions for each value in p
    pos = [0] * (n + 1)
    for i in range(n):
        pos[p[i]] = i + 1
    
    # Check for cycles
    visited = [False] * (n + 1)
    for i in range(1, n + 1):
        if not visited[i]:
            cycle_length = 0
            x = i
            while not visited[x]:
                visited[x] = True
                x = p[x - 1]
                cycle_length += 1
            
            # If any cycle has an odd length, return -1
            if cycle_length % 2 != 0:
                return [-1]
    
    # Construct the permutation q
    q = [0] * n
    visited = [False] * (n + 1)
    for i in range(1, n + 1):
        if not visited[i]:
            cycle = []
            x = i
            while not visited[x]:
                visited[x] = True
                cycle.append(x)
                x = p[x - 1]
            
            # Pair up elements in the cycle
            for j in range(len(cycle)):
                q[pos[cycle[j]] - 1] = cycle[(j + 1) % len(cycle)]
    
    return q

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
p = list(map(int, data[1:]))

# Find and print the permutation q
result = find_permutation(n, p)
if result == [-1]:
    print(-1)
else:
    print(" ".join(map(str, result)))