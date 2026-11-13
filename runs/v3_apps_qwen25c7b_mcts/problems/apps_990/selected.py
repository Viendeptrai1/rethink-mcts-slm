import sys
from collections import defaultdict

def count_valid_paintings(n, edges, m, restrictions):
    # Build the adjacency list for the tree
    adj_list = defaultdict(list)
    for a, b in edges:
        adj_list[a].append(b)
        adj_list[b].append(a)

    def dfs(node, parent, color):
        nonlocal valid
        if node == restrictions[0][0]:
            if color != 'B':
                return False
        elif node == restrictions[0][1]:
            if color != 'B':
                return False
        for neighbor in adj_list[node]:
            if neighbor == parent:
                continue
            if not dfs(neighbor, node, 'W' if color == 'B' else 'B'):
                return False
        return True

    valid = False
    for start_color in ['W', 'B']:
        if dfs(1, -1, start_color):
            valid = True
            break

    return int(valid)

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
edges = [(int(data[i*2+1]), int(data[i*2+2])) for i in range(n-1)]
m = int(data[n*2+1])
restrictions = [(int(data[(n+i)*2+2]), int(data[(n+i)*2+3])) for i in range(m)]

# Calculate and print the result
result = count_valid_paintings(n, edges, m, restrictions)
print(result)