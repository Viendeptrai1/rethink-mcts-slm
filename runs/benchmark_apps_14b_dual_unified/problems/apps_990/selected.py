import sys
from collections import defaultdict

def dfs(node, parent, colors, restrictions, graph):
    count = 1
    for neighbor in graph[node]:
        if neighbor != parent:
            for color in range(2):
                colors[(node, neighbor)] = color
                valid = True
                for u, v in restrictions:
                    if not is_path_black(u, v, node, neighbor, colors, graph):
                        valid = False
                        break
                if valid:
                    count += dfs(neighbor, node, colors, restrictions, graph)
            colors.pop((node, neighbor))
    return count

def is_path_black(u, v, start, end, colors, graph):
    visited = set()
    stack = [(start, [start])]
    while stack:
        node, path = stack.pop()
        if node == v:
            for i in range(len(path) - 1):
                if colors.get((path[i], path[i + 1]), 0) == 0 and colors.get((path[i + 1], path[i]), 0) == 0:
                    return False
            return True
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor != end and neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))
    return False

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    index += 1
    
    graph = defaultdict(list)
    for _ in range(N - 1):
        a = int(data[index])
        b = int(data[index + 1])
        graph[a].append(b)
        graph[b].append(a)
        index += 2
    
    M = int(data[index])
    index += 1
    
    restrictions = []
    for _ in range(M):
        u = int(data[index])
        v = int(data[index + 1])
        restrictions.append((u, v))
        index += 2
    
    colors = {}
    result = dfs(1, -1, colors, restrictions, graph)
    print(result)

if __name__ == "__main__":
    main()