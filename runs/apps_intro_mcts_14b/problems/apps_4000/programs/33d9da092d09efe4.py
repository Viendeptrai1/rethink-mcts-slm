import sys
from collections import defaultdict

def dfs(node, parent, graph, depth):
    max_depth = depth
    farthest_node = node
    for neighbor in graph[node]:
        if neighbor != parent:
            child_depth, child_farthest = dfs(neighbor, node, graph, depth + 1)
            if child_depth > max_depth:
                max_depth = child_depth
                farthest_node = child_farthest
    return max_depth, farthest_node

def find_longest_paths(graph, n):
    # Find the first longest path
    _, farthest_node = dfs(1, -1, graph, 0)
    # Find the second longest path starting from the farthest node of the first path
    _, second_farthest_node = dfs(farthest_node, -1, graph, 0)
    # Find the third longest path starting from the farthest node of the second path
    _, third_farthest_node = dfs(second_farthest_node, -1, graph, 0)
    
    return farthest_node, second_farthest_node, third_farthest_node

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    graph = defaultdict(list)
    
    index = 1
    for _ in range(n - 1):
        a = int(data[index])
        b = int(data[index + 1])
        graph[a].append(b)
        graph[b].append(a)
        index += 2
    
    a, b, c = find_longest_paths(graph, n)
    
    res = len(graph[a]) + len(graph[b]) + len(graph[c]) - 6
    print(res)
    print(a, b, c)

if __name__ == "__main__":
    main()