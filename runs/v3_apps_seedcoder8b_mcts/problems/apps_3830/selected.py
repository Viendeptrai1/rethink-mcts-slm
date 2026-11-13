import sys
from collections import defaultdict, deque

sys.setrecursionlimit(300000)

def find_sccs(n, graph, reverse_graph):
    visited = [False] * n
    stack = []

    def fill_order(v):
        visited[v] = True
        for u in graph[v]:
            if not visited[u]:
                fill_order(u)
        stack.append(v)

    def dfs(v, component):
        visited[v] = True
        component.append(v)
        for u in reverse_graph[v]:
            if not visited[u]:
                dfs(u, component)

    for i in range(n):
        if not visited[i]:
            fill_order(i)

    visited = [False] * n
    sccs = []

    while stack:
        v = stack.pop()
        if not visited[v]:
            component = []
            dfs(v, component)
            sccs.append(component)

    return sccs

def count_returnable_rooms(n, s):
    graph = defaultdict(list)
    reverse_graph = defaultdict(list)

    for i in range(n):
        if s[i] == '>' or s[i] == '-':
            graph[i].append((i + 1) % n)
            reverse_graph[(i + 1) % n].append(i)
        if s[i] == '<' or s[i] == '-':
            graph[(i + 1) % n].append(i)
            reverse_graph[i].append((i + 1) % n)

    sccs = find_sccs(n, graph, reverse_graph)
    returnable_count = 0

    for scc in sccs:
        if len(scc) > 1 or (len(scc) == 1 and s[scc[0]] == '-'):
            returnable_count += len(scc)

    return returnable_count

def main():
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    t = int(data[index])
    index += 1
    results = []

    for _ in range(t):
        n = int(data[index])
        index += 1
        s = data[index]
        index += 1
        result = count_returnable_rooms(n, s)
        results.append(result)

    for res in results:
        print(res)

if __name__ == "__main__":
    main()