import sys
from collections import defaultdict

def read_input():
    n = int(sys.stdin.readline().strip())
    fragments = [sys.stdin.readline().strip() for _ in range(n)]
    return n, fragments

def build_graph(fragments):
    graph = defaultdict(list)
    for i, frag1 in enumerate(fragments):
        for j, frag2 in enumerate(fragments):
            if i != j and frag1.endswith(frag2[:5]):
                graph[i].append(j)
    return graph

def dfs(graph, start, visited, stack):
    visited[start] = True
    for neighbor in graph[start]:
        if not visited[neighbor]:
            dfs(graph, neighbor, visited, stack)
    stack.append(start)

def topological_sort(graph, n):
    visited = [False] * n
    stack = []
    for i in range(n):
        if not visited[i]:
            dfs(graph, i, visited, stack)
    return stack[::-1]

def reconstruct_text(fragments, order):
    result = fragments[order[0]]
    for i in range(1, len(order)):
        overlap_length = min(len(fragments[order[i]]), 5)
        while fragments[order[i]][overlap_length:] == fragments[order[i-1]][:overlap_length]:
            overlap_length -= 1
        result += fragments[order[i]][overlap_length:]
    return result

def main():
    n, fragments = read_input()
    graph = build_graph(fragments)
    order = topological_sort(graph, n)
    
    # Check for cycles
    visited = [False] * n
    rec_stack = [False] * n
    def detect_cycle(node):
        visited[node] = True
        rec_stack[node] = True
        for neighbor in graph[node]:
            if not visited[neighbor] and detect_cycle(neighbor):
                return True
            elif rec_stack[neighbor]:
                return True
        rec_stack[node] = False
        return False
    
    if any(detect_cycle(i) for i in range(n)):
        print("AMBIGUOUS")
        return
    
    reconstructed_text = reconstruct_text(fragments, order)
    print(reconstructed_text)

if __name__ == "__main__":
    main()