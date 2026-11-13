from sys import stdin, stdout
import sys
sys.setrecursionlimit(10**6)

def dfs(node, parent, jokes, visited, joke_set):
    visited[node] = True
    joke_set.add(jokes[node-1])
    
    for neighbor in graph[node]:
        if neighbor != parent and not visited[neighbor]:
            if not dfs(neighbor, node, jokes, visited, joke_set):
                return False
    
    if len(joke_set) > 1 and max(joke_set) - min(joke_set) != len(joke_set) - 1:
        return False
    
    return True

def count_sets(n, jokes, edges):
    global graph
    graph = [[] for _ in range(n+1)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    visited = [False] * (n+1)
    total_sets = 0
    
    def backtrack(start):
        nonlocal total_sets
        if start == n + 1:
            total_sets += 1
            return
        
        for i in range(start, n + 1):
            if not visited[i]:
                visited[i] = True
                if dfs(i, None, jokes, visited, set()):
                    backtrack(i + 1)
                visited[i] = False
    
    backtrack(1)
    return total_sets

# Read input
input = stdin.read
data = input().split()
n = int(data[0])
jokes = list(map(int, data[1:n+1]))
edges = []
for i in range(n-1):
    u = int(data[n+i*2+1])
    v = int(data[n+i*2+2])
    edges.append((u, v))

# Output result
stdout.write(str(count_sets(n, jokes, edges)) + '\n')