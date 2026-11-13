from sys import stdin, stdout
import itertools

def count_valid_paintings(N, edges, M, restrictions):
    def dfs(node, parent, color):
        nonlocal valid
        if node == target:
            valid = True
            return
        for neighbor, _color in adj[node]:
            if neighbor != parent and color ^ _color:
                dfs(neighbor, node, color ^ _color)
    
    adj = [[] for _ in range(N)]
    for a, b in edges:
        adj[a-1].append((b-1, 0))
        adj[b-1].append((a-1, 0))
    
    result = 0
    for coloring in itertools.product([0, 1], repeat=len(edges)):
        valid = False
        for i, (u, v) in enumerate(restrictions):
            u -= 1
            v -= 1
            target = u
            dfs(v, -1, coloring[i])
            if not valid:
                break
        if valid:
            result += 1
    
    return result

# Read input
N = int(stdin.readline())
edges = [tuple(map(int, stdin.readline().split())) for _ in range(N-1)]
M = int(stdin.readline())
restrictions = [tuple(map(int, stdin.readline().split())) for _ in range(M)]

# Print output
stdout.write(str(count_valid_paintings(N, edges, M, restrictions)) + '\n')