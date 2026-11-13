def find_inverse_permutation(p):
    n = len(p)
    visited = [False] * (n + 1)
    result = [-1] * n
    
    for i in range(1, n + 1):
        if not visited[i]:
            cycle = []
            x = i
            while not visited[x]:
                visited[x] = True
                cycle.append(x)
                x = p[x - 1]
            
            if len(cycle) % 2 != 0:
                return -1
            
            half_cycle_length = len(cycle) // 2
            for j in range(half_cycle_length):
                result[cycle[j] - 1] = cycle[half_cycle_length + j]
                result[cycle[half_cycle_length + j] - 1] = cycle[j]
    
    return result

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
p = list(map(int, data[1:]))

# Find the inverse permutation
result = find_inverse_permutation(p)

# Print the result
if result == -1:
    print(-1)
else:
    print(" ".join(map(str, result)))