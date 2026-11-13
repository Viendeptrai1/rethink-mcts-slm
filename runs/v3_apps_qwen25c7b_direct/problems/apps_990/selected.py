from sys import stdin, stdout
from collections import defaultdict

def dfs(node, parent, color):
    global valid
    for neighbor in graph[node]:
        if neighbor == parent:
            continue
        if color[node] == color[neighbor]:
            valid = False
            return
        dfs(neighbor, node, 1 - color[node])

def count_ways():
    n = int(stdin.readline())
    graph = defaultdict(list)
    for _ in range(n - 1):
        a, b = map(int, stdin.readline().split())
        graph[a].append(b)
        graph[b].append(a)
    
    m = int(stdin.readline())
    restrictions = [tuple(map(int, stdin.readline().split())) for _ in range(m)]
    
    total_ways = 0
    
    def check_coloring(color):
        nonlocal valid
        valid = True
        for u, v in restrictions:
            stack = [u]
            visited = set()
            while stack:
                node = stack.pop()
                if node in visited:
                    continue
                visited.add(node)
                for neighbor in graph[node]:
                    if neighbor == v:
                        break
                    stack.append(neighbor)
            else:
                return False
        return True
    
    def backtrack(node, parent, color):
        nonlocal total_ways
        if node == n + 1:
            if check_coloring(color):
                total_ways += 1
            return
        for c in range(2):
            color[node] = c
            dfs(node, parent, color)
            if valid:
                backtrack(node + 1, node, color)
            color[node] = 1 - c
    
    backtrack(1, None, [0] * (n + 1))
    
    stdout.write(str(total_ways) + '\n')

count_ways()