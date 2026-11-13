import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])

edges = []
for i in range(m):
    u = int(data[2 + 2 * i]) - 1
    v = int(data[3 + 2 * i]) - 1
    edges.append((u, v))

def can_orientate_graph():
    # Check if the graph can be oriented without creating paths of length two or more
    # We will try to orient all edges away from the root node (arbitrarily chosen)
    root = 0
    visited = [False] * n
    stack = [root]
    while stack:
        current = stack.pop()
        if visited[current]:
            continue
        visited[current] = True
        for neighbor in range(n):
            if not visited[neighbor] and (current, neighbor) in edges:
                return False
            elif not visited[neighbor] and (neighbor, current) in edges:
                stack.append(neighbor)
    return True

if can_orientate_graph():
    print("YES")
    orientation = ['0'] * m
    root = 0
    visited = [False] * n
    stack = [root]
    while stack:
        current = stack.pop()
        if visited[current]:
            continue
        visited[current] = True
        for i, (u, v) in enumerate(edges):
            if u == current:
                orientation[i] = '1'
            elif v == current:
                orientation[i] = '0'
            if not visited[u] and u != current:
                stack.append(u)
            if not visited[v] and v != current:
                stack.append(v)
    print(''.join(orientation))
else:
    print("NO")